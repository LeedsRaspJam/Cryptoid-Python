#!/bin/bash

echo '                                           __                __        __ '
echo '                                          /  |              /  |      /  |'
echo '  _______   ______   __    __   ______   _%% |_     ______  %%/   ____%% |'
echo ' /       | /      \ /  |  /  | /      \ / %%   |   /      \ /  | /    %% |'
echo '/%%%%%%%/ /%%%%%%  |%% |  %% |/%%%%%%  |%%%%%%/   /%%%%%%  |%% |/%%%%%%% |'
echo '%% |      %% |  %%/ %% |  %% |%% |  %% |  %% | __ %% |  %% |%% |%% |  %% |'
echo '%% \_____ %% |      %% \__%% |%% |__%% |  %% |/  |%% \__%% |%% |%% \__%% |'
echo '%%       |%% |      %%    %% |%%    %%/   %%  %%/ %%    %%/ %% |%%    %% |'
echo ' %%%%%%%/ %%/        %%%%%%% |%%%%%%%/     %%%%/   %%%%%%/  %%/  %%%%%%%/'
echo '                    /  \__%% |%% |'
echo '                    %%    %%/ %% |'
echo '                     %%%%%%/  %%/'
echo 

echo 'Downloading Latest Build...'
git pull --quiet

echo -n 'Current version: '
git show --format="%h" --no-patch > version.txt
cat version.txt

echo 'Updating dependencies...'
pip3 install -q -r requirements.txt

echo 'Executing program...'
python3 main.py