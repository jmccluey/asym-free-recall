function report_file = crp_report_asymFR(data, res_dir, report_name, ...
                                         compile)
%CRP_REPORT_ASYMFR  Behavioral CRP report for asymFR, across categories.
%
%  report_file = crp_report_asymFR(data, res_dir, report_name, compile)
%
%  INPUTS:
%          data:  asymFR data structure
%       res_dir:  directory in which to place the resulting report,
%                 e.g., '~/reports/asymfr'
%   report_name:  file name for the LaTeX report ('asymfr_crp_report')
%       compile:  compile LaTeX report (true)
%
%  OUTPUT:
%   report_file:  filename of the resulting PDF report

% input checks
if ~exist('data','var')
  error('You must pass a fr_data structure.')
end
if ~exist('res_dir','var')
  error('You must give the path to a results directory.')
end
if ~exist('report_name','var')
  report_name = 'asymfr_crp_report';
end
if ~exist('compile','var')
  compile = true;
end

% prepare directory structure for the report
if ~exist(res_dir,'dir')
  mkdir(res_dir)
end

% figure filenames will be relative to res_dir
cd(res_dir)

% prepare the figures directory
fig_dir = 'figs';
if ~exist(sprintf('./%s',fig_dir),'dir')
  mkdir(fig_dir)
end

LINETYPE = {'solid'};
LABEL = {};
PRINT = {'-depsc'};


% get subject ids and number of trials for each
subjects = unique(data.subjid);
n_subj = length(subjects);
subject_labels = cell(size(subjects));
fig_files = [];

fprintf('Making plots for:\n')
for i=1:length(subjects)
  fprintf('%s\n', subjects{i})
  subject_labels{i} = sprintf('%s', subjects{i});
end
fprintf('\n')

% do the analyses
res = analyze_asymFR(data);

%%% SPC %%%
% animals
% make grand average and subject plots
f = @plot_crp;
f_in = {};
[ga_file, subj_files] = plot_ga_subj(res.anim.crp.subj, subjects, f, f_in, fig_dir, 'crp_anim_%s.eps', PRINT);

% add to our list of files
fig_files = add_fig_files(fig_files, 'ANIM', {ga_file, subj_files{:}});

% food
% make grand average and subject plots
f = @plot_crp;
f_in = {};
[ga_file, subj_files] = plot_ga_subj(res.food.crp.subj, subjects, f, f_in, fig_dir, 'crp_food_%s.eps', PRINT);

% add to our list of files
fig_files = add_fig_files(fig_files, 'FOOD', {ga_file, subj_files{:}});

% tool
% make grand average and subject plots
f = @plot_crp;
f_in = {};
[ga_file, subj_files] = plot_ga_subj(res.tool.crp.subj, subjects, f, f_in, fig_dir, 'crp_tool_%s.eps', PRINT);

% add to our list of files
fig_files = add_fig_files(fig_files, 'TOOL', {ga_file, subj_files{:}});

% vehi
% make grand average and subject plots
f = @plot_crp;
f_in = {};
[ga_file, subj_files] = plot_ga_subj(res.vehi.crp.subj, subjects, f, f_in, fig_dir, 'crp_vehi_%s.eps', PRINT);

% add to our list of files
fig_files = add_fig_files(fig_files, 'VEHI', {ga_file, subj_files{:}});


% REPORT
% make a LaTeX table with all figures
fig_table = squeeze(struct2cell(fig_files))';
ga_label = sprintf('Grand Average (%d)', length(subjects));
table = create_report(fig_table, {ga_label, subject_labels{:}});
analyses = fieldnames(fig_files);
header = {'Subject ($N$)', analyses{:}};

% make a LaTeX document
report_ltx = fullfile(res_dir, report_name);
landscape = false;
longtable(table, header, report_ltx, 'AsymFR CRP Report', landscape);

% compile
if compile
  pdf_file = pdflatex(report_ltx);
  report_file = pdf_file;
  fprintf('saved in %s.\n', report_file)
end





function [ga_file, subj_files] = plot_ga_subj(matrix, subjects, f, f_inputs, res_dir, filename, print_in)
  %PLOT_GA_SUBJ   Make subject and grand average plots, and print them.
  %
  %  INPUTS:
  %      matrix:  a subjects X trials X ... matrix
  %
  %    subjects:  a cell array of subject identifiers.
  %
  %           f:  a handle to a function that takes in a trials X distractor_lens
  %               matrix, and makes a plot.
  %
  %    f_inputs:  cell array of additional inputs to f.
  %
  %     res_dir:  directory in which to save the plots.
  %
  %    filename:  base name of the files; each is created using
  %               sprintf(filename, [subject id]), so filename
  %               should include a %s.
  % 
  %    print_in:  additional input to the print command.
  %
  %  OUTPUTS:
  %     ga_file:  path to the file where the grand average plot is saved.
  %
  %  subj_files:  cell array of filenames for each subject.

  % grand average
  clf
  ga_file = fullfile(res_dir, sprintf(filename, 'ga'));
  f(squeeze(nanmean(matrix, 1)), f_inputs{:});
  print(gcf, print_in{:}, ga_file)
  
  % subjects
  for i=1:length(subjects)
    clf
    subj_files{i} = fullfile(res_dir, sprintf(filename, subjects{i}));
    f(squeeze(matrix(i,:)), f_inputs{:});
    print(gcf, print_in{:}, subj_files{i})
  end
%endfunction

function fig_files = add_fig_files(fig_files, field, files)
  %ADD_FIG_FILES   Add figure paths to the fig_files structure.
  %
  %  INPUTS:
  %  fig_files:
  %
  %  field:
  %
  %  files:
  %
  %  OUTPUTS:
  %  fig_files:
  
  [fig_files(1:length(files)).(field)] = deal(files{:});
%endfunction