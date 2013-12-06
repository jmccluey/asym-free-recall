function exp = asymfr3(varargin)
%ASYMFR   Creates exp structure for Asymmetry Free Recall
%
%  Creates events for any sessions that are new or have modified
%  annotate files. Creates events and data structures for all
%  subjects. Saves an eeg_ana-compatible experiment in res_dir.
%
%  exp = asymfr3(...)
%
%  PARAMS:
%  May be specified using property, value pairs. Defaults are shown
%  in parentheses.
%   dataroot     - path to directory where subject data directories
%                  are located ('data/beh/asymFR3')
%   res_dir      - path to directory where results will be saved.
%                  ('data/beh/asymFR3')
%   force_events - logical indicating whether to force creation of
%                  events for all sessions, regardless of whether
%                  the source files have been modified (false)

% options
defaults.dataroot = '/data/beh/asymFR3';
defaults.res_dir = defaults.dataroot;
defaults.force_events = false;
params = propval(varargin, defaults);

params.dataroot = check_dir(params.dataroot);
params.res_dir = check_dir(params.res_dir);

% find sessions
subj = get_sessdirs(params.dataroot, 'ASM*', {'session.log'});
exp = init_exp('asymFR3', 'subj', subj, 'resDir', params.res_dir);

% create events
if params.force_events
  inputs = {'force', true};
else
  inputs = {};
end
exp.subj = apply_to_subj(exp.subj, @create_events, ...
                         {@create_events_asymfr, {}, inputs{:}});

% import events
events_dir = fullfile(params.res_dir, 'beh', 'all');
exp.subj = apply_to_subj(exp.subj, @import_events, ...
                         {'all', events_dir});

% concatenate
exp = cat_all_subj_events(exp, 'all');
exp.subj = apply_to_ev(exp.subj, 'all', @create_data, ...
                       {'data', 'f', @FRdata});
exp = cat_all_subj_data(exp, {'ev', 'all', 'stat', 'data'});

% update
exp = update_exp(exp, ...
                 'created asymFR exp object with events and data structures');