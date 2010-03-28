Infraero (Brazilian air control department) web data collector.

Developed during the Yahoo! BR Hack Day 2010.

Usage:

import Infraero
infra = Infraero.Harvester()
flight = infra.request_flight('SBSP', 3100)
airport = infra.request_airport('SBSP')

A running example at:
http://test1.bento.eti.br/infraero/

Copyright 2010 Danilo Ehrhardt Ferreira Bento

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. 
