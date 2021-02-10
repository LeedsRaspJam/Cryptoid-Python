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

echo Downloading Latest Build...
git pull --quiet
echo Updating dependencies...
pip3 install -p -r requirements.txt
echo Executing program...
python3 main.py