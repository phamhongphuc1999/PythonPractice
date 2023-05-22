#!/bin/bash

# Download NASA logs data
wget -q -P data --show-progress ftp://ita.ee.lbl.gov/traces/NASA_access_log_Jul95.gz
wget -q -P data --show-progress ftp://ita.ee.lbl.gov/traces/NASA_access_log_Aug95.gz

# Unzip file
tar -xf data/NASA_access_log_Aug95.gz
tar -xf data/NASA_access_log_Jul95.gz
