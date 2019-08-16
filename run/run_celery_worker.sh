#!/bin/bash

cd project
celery worker -A celery  
