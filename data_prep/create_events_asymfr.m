function events = create_events_asymfr(sess_dir, subject, session)
%CREATE_EVENTS_ASYMFR   Create an events structure for a session of
%                       Asymmetry Free Recall
%
%  events = create_events_asymfr(sess_dir, subject, session)
%
%  INPUTS:
%  sess_dir:  path to the directory containing data for the session.
%
%   subject:  string identifier of the subject.
%
%   session:  number of the session (zero-indexed).
%
%  OUTPUTS:
%   events:  a structure with one element for each event in the
%            experiment. See below for details.
%
%  EVENTS:
%  The "type" field indicates the general type of each
%  event. Possible types are:
%   WORD      - word study presentation
%   REC_START - start of a free recall period
%   REC_WORD  - attempt at a recall (or vocalization if item='VV')
%   FFR_REC_WORD - attempt at a final free recall (or vocalization
%                  if item='VV')
%
%  Each event has a number of fields. Fields are:
%   subject          - string identifier of the subject
%   session          - session number
%   trial            - trial number
%   type             - type of the event (see above)
%   list             - string identifier of word list
%   serialpos        - serial position in which word was presented
%                      during the study list
%   endmathcorrect - for WORD events, number of correct math problems
%   endnumproblems - for WORD events, number of math problems completed
%   item             - string of the word presented or recalled
%   itemno           - index of the word in the wordpool
%   recalled         - 1 (word subsequently recalled), 0 (not recalled)
%   finalrecalled    - 1 (subsequently recalled during FFR), or 0
%   rectime          - time (in ms) after beginning of the recall
%                      period that the word was vocalized
%   intrusion        - 0 (correct recall), -1 (intrusion; XLI or PLI)
%   mstime           - time of the event in absolute experiment time
%   msoffset         - estimated maximum possible error of mstime

% input checks
if ~exist('sess_dir', 'var') || ~ischar(sess_dir)
  error('You must pass the path to a session directory.')
end
if ~exist('subject', 'var')
  warning('EventsCreation:noSubjectId', ...
          'No subject id specified. "subject" field will be empty.')
  subject = '';
end
if ~exist('session', 'var')
  warning('EventsCreation:noSessionNumber', ...
          'No session number specified. "session" field will be empty.')
  session = [];
end

% get the number of header lines to exclude from the log file
% this is necessary for times when the session was started then
% immediately quit to prepare stimuli before a session
session_log_file = fullfile(sess_dir, 'session.log');
temp = read_session_log(session_log_file, {'mstime', 'msoffset', 'type'}, ...
                       {'%n', '%n', '%s'});
header_lines = max([find(strcmp({temp.type}, 'SESS_START')) 0]);

% read the log file
fields = {'mstime' 'msoffset' 'type' 'trial' 'list_name' 'item' 'itemno'};
format = {'%n'     '%n'       '%s'   '%n'    '%s'       '%s'   '%n'};
full_log = read_session_log(session_log_file, fields, format, ...
                            'header_lines', header_lines);

% struct to keep track of experiment state
current.subject = subject;
current.session = session + 1;
current.block = '';
current.trial = NaN;
current.list_pos = NaN;
current.list_name = '';
%current.distractor = NaN;
current.mathcorrect = NaN;
current.numproblems = NaN;

% step through the logfile, adding events as necessary
events = [];
for log=full_log
  switch log.type
    
    % BLOCK STARTS
   case 'SESS_START'
    current.block = 'fr';
   
   case 'FFR_START'
    current.block = 'ffr';

   case 'FR_PRES'
    if current.trial ~= log.trial + 1
      % start of a new list
      current.trial = log.trial + 1;
      current.list_pos = 1;
      current.list_name = log.list_name;
      list_study_events = [];
    end
    
    % assume no distractor until we encounter one.  This may have
    % already been set by a just-prior DISTRACTOR event, in which
    % case current.distractor will be non-NaN.
    %if isnan(current.distractor)
    %  current.distractor=0;
    %end
    
    % word presentation event
    event = event_template(current, log, 'WORD');
    event.item = upper(deblank(log.item));
    event.itemno = log.itemno;
    event.list = log.list_name;
    event.serialpos = current.list_pos;
    
    % move to next item
    current.list_pos = current.list_pos + 1;
    list_study_events = [list_study_events event];
    
   case 'DISTRACTOR'
    % hold current values
    current.mathcorrect = log.itemno;
    current.numproblems = str2num(log.item);
    
   case 'REC_START'
    if strcmp(current.block, 'fr')
      % end of item presentations
      % sanity check the list items
      list_items = {list_study_events.item};
      uniq_items = unique(list_items);
      if length(list_items) > length(uniq_items)
        error(['List %d has repeated items. Did you stop and restart the '   ...
               'experiment?\nIf so, you may have extra lines in your '       ...
               'session.log. Backup the log, delete the lines, and retry.'], ...
              current.trial)
      end
      
      % set end-of-list distractor
      [list_study_events.endmathcorrect] = ...
          deal(current.mathcorrect);
      [list_study_events.endnumproblems] = ...
          deal(current.numproblems);
    end
    
    % reset distractor
    current.distractor = NaN;
    current.mathcorrect = NaN;
    
    % read the annotate file
    file_name = get_ann_file_name(current.block, current.trial);
    ann_file = fullfile(sess_dir, file_name);
    
    if ~exist(ann_file, 'file')
      % no annotation yet; just include study events
      fprintf('Warning: missing annotate file: %s\n', ann_file)
      rec_start_event = event_template(current, log, 'REC_START');
      rec_start_event.list = current.list_name;
      
      if strcmp(current.block, 'fr')
        events = [events list_study_events rec_start_event];
      else
        rec_start_event.trial = NaN;
      end
      
      continue % skip to next log line
    end
    
    % annotate file exists
    % recall period has been annotated, so recalled field is
    % defined
    
    if strcmp(current.block, 'fr')
      [list_study_events.recalled] = deal(0);
      fr_events = read_free_recall(list_study_events, log.mstime, ...
                                  ann_file);
      
      % recalled field undefined for REC_START
      fr_events(strcmp({fr_events.type}, 'REC_START')).recalled = ...
          NaN;
      % set list name
      fr_events(strcmp({fr_events.type}, 'REC_START')).list = ...
          deal(current.list_name);
            
      % set the subsequent memory field on study events
      recalled = ~isnan([fr_events.rectime]) & strcmp({fr_events.type}, ...
                                                      'WORD');
      [fr_events(recalled).recalled] = deal(1);
      
      events = [events fr_events];
    else
      % FFR
      ispres = strcmp({events.type},'WORD');
      study_events = events(ispres);
      
      ffr_events = read_free_recall(study_events, log.mstime, ...
                                    ann_file);
      
      % REC_START event
      rec_start_event = ffr_events(strcmp({ffr_events.type}, ...
                                          'REC_START'));
      rec_start_event.list = 'ffr';
      rec_start_event.recalled = NaN;
      
      % FFR_REC_WORD events
      ffr_rec_events = ffr_events(strcmp({ffr_events.type}, ...
                                         'REC_WORD'));
      [ffr_rec_events(:).type] = deal('FFR_REC_WORD');
      
      % set the subsequent memory field on study events
      ffr_study_events = ffr_events(strcmp({ffr_events.type}, ...
                                           'WORD'));
      finalrecalled = ~isnan([ffr_study_events.rectime]);
      finalrecalled =  num2cell(finalrecalled);
      [events(ispres).finalrecalled] = deal(finalrecalled{:});
      
      events = [events rec_start_event ffr_rec_events];
      
    end
  end
end

% sort to put events into order
events = sort_events(events);

function event = event_template(current, log, event_type)
  %EVENT_TEMPLATE   Make a default event.
  %
  %  event = event_template(current, log, event_type)
  %
  %  This function does everything that must be done for each
  %  event, regardless of what is happening in the experiment.
  
  % input checks
  if ~exist('current', 'var') || ~isstruct(current)
    error('You must pass a structure with current info.')
  elseif ~exist('log', 'var') || ~ isstruct(log)
    error('You must pass a structure with the current line of the log.')
  end
  if ~exist('event_type', 'var')
    error('You must specify an event type.')
  end
  
  % set defaults for each field of the events structure
  event = struct('subject',           current.subject, ...
                 'session',           current.session, ...
                 'trial',             current.trial,   ...
                 'type',              event_type,      ...
                 'list',              '',              ...
                 'serialpos',         NaN,             ...
                 'endmathcorrect',    NaN,             ...
                 'endnumproblems',    NaN,             ...
                 'item',              '',              ...
                 'itemno',            NaN,             ...
                 'recalled',          NaN,             ...
                 'finalrecalled',     NaN,             ...
                 'rectime',           NaN,             ...
                 'intrusion',         NaN,             ...
                 'mstime',            log.mstime,      ...
                 'msoffset',          log.msoffset);

function file_name = get_ann_file_name(trial_type, trial_number, ...
                                                   file_type)
  %GET_ANN_FILE_NAME  Get the file name for an annotate file
  %
  %  file_name = get_ann_file_name(trial_type, trial_number,
  %  file_type)
  
  % input checks
  if ~exist('trial_type', 'var')
    error('You must pass a trial type.')
  end
  if ~exist('trial_number', 'var') || isnan(trial_number)
    trial_number = [];
  end
  if ~exist('file_type', 'var')
    file_type = 'ann';
  end
  
  % define the file name prefix
  switch trial_type
   case 'fr'
    prefix = '';
    trial_number = trial_number - 1;
   case 'ffr'
    prefix = 'ffr';
    trial_number = [];
  end
  
  % write the filename
  file_name = sprintf('%s%d.%s', prefix, trial_number, file_type);
    
    