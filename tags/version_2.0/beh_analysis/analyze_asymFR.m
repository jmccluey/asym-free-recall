function res = analyze_asymFR(data)
%ANALYZE_ASYMFR  Run beh analyses on asymFR data
%
%  res = analyze_asymFR(data)
%
%  INPUT:
%   data:  data structure of asymFR data
%
%  OUTPUT:
%    res:  structure containing results of analyses for various
%          subsets of data
%

% remove practice trial, add listtype
data = prep_data_asymFR(data);

% run analyses on subsets
res = [];

% overall results
res.overall = analyze_subset_asymFR(data);

% less-related
data_gen = trial_subset(data.listtype==0,data);
res.gen = analyze_subset_asymFR(data_gen);

% more-related
data_spec = trial_subset(data.listtype==1,data);
res.spec = analyze_subset_asymFR(data_spec);

% animals
anim_lists = {'anim_gen1', 'anim_gen2', 'anim_farm', 'anim_sea'};
data_anim = trial_subset(ismember(data.pres.list(:,1), anim_lists), ...
                         data);
res.anim = analyze_subset_asymFR(data_anim);

% food
food_lists = {'food_gen1', 'food_gen2', 'food_fruit', 'food_junk'};
data_food = trial_subset(ismember(data.pres.list(:,1), food_lists), ...
                         data);
res.food = analyze_subset_asymFR(data_food);

% tools
tool_lists = {'tool_gen1', 'tool_gen2', 'tool_carp', 'tool_gard'};
data_tool = trial_subset(ismember(data.pres.list(:,1), tool_lists), ...
                         data);
res.tool = analyze_subset_asymFR(data_tool);

% vehicles
vehi_lists = {'vehi_gen1', 'vehi_gen2', 'vehi_land'};
data_vehi = trial_subset(ismember(data.pres.list(:,1), vehi_lists), ...
                         data);
res.vehi = analyze_subset_asymFR(data_vehi);


% analysis
function res = analyze_subset_asymFR(data)
%ANALYZE_SUBSET_ASYMFR  Run beh analyses on subset of asymFR data
%
%  res.sub = analyze_subset_asymFR(data)
%
%  INPUT:
%       data:  data structure of subset of asymFR data
%
%  OUTPUT:
%    res.sub:  structure containing subset analysis results
%

res = [];

% PREC
res.prec.subj = p_rec(data.recalls, data.subject, data.listLength);
res.prec.m = nanmean(res.prec.subj,1);
res.prec.sem = nanstd(res.prec.subj,1) / sqrt(size(res.prec.subj,1));

% SPC
res.spc.subj = spc(data.recalls, data.subject, data.listLength);
res.spc.m = nanmean(res.spc.subj,1);

% PFR
res.pfr.subj = pfr(data.recalls, data.subject, data.listLength);
res.pfr.m = nanmean(res.pfr.subj,1);

% CRP
res.crp.subj = crp(data.recalls, data.subject, data.listLength);
res.crp.m = nanmean(res.crp.subj,1);

% ASYM
mid_col = (size(res.crp.subj,2)-1)/2 + 1;
asym_subj = res.crp.subj(:,mid_col+1) - res.crp.subj(:,mid_col- ...
                                                  1);

res.asym.subj = asym_subj ./ (res.crp.subj(:,mid_col+1) + ...
                               res.crp.subj(:,mid_col-1));
res.asym.m = nanmean(res.asym.subj,1);
res.asym.sem = nanstd(res.asym.subj,1) / sqrt(size(res.asym.subj, ...
                                                  1));