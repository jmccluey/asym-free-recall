function data = prep_data_asymFR(data)
%PREP_DATA_ASYMFR  Prepares behavioral data for asymFR for analysis
%
%  data = prep_data_asymFR(data)
%
%  INPUT:
%   data:  asymFR behavioral data structure
%
%  OUTPUT:
%   data:  data structure, with practice trial removed, and added
%          listtype:
%           0 = general, less-related
%           1 = specific, more-related
%

% remove practice trial
data = trial_subset(data.pres.trial(:,1)>1, data);

% specify "general" (less-related) and "specific" (more-related) lists
cat_gen = {'anim_gen1', 'anim_gen2', 'food_gen1', 'food_gen2', ...
           'tool_gen1', 'tool_gen2', 'vehi_gen1', 'vehi_gen2'};

cat_spec = {'anim_farm', 'anim_sea', 'food_fruit', 'food_junk', ...
            'tool_carp', 'tool_gard', 'vehi_land'};

% listtype
% 0 = less-related
% 1 = more-related
data.listtype = NaN(size(data.recalls,1),1);
data.listtype(ismember(data.pres.list(:,1), cat_gen)) = 0;
data.listtype(ismember(data.pres.list(:,1), cat_spec)) = 1;

