#!/usr/bin/python
'''
Created on 2010-03-20

@author: Danilo Ehrhardt Ferreira Bento <danilo@bento,eti.br>

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

Usage:

import Infraero
infra = Infraero.Harvester()
flight = infra.request_flight('SBSP', 3100)
airport = infra.request_airport('SBSP')
'''
__all__ = ['Harvester','Formater']

import cookielib
import urllib2
import urllib
from HTMLParser import HTMLParser
import re

class RequestVarsHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.requestvars = []

    def handle_starttag(self, tag, attrs):
        if (tag == 'input'):
            dic = dict(attrs)
            if dic.get('name') in ['__VIEWSTATE', '__EVENTVALIDATION']:
                self.requestvars.append(tuple([dic.get('name'),dic.get('value')]))
                
    def get_request_vars(self):
        return self.requestvars

class FlightDataHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.openspan = ''
        self.openpagination = False
        self.flightdata = []
        self.flights = []
        self.pagedate = ''
        self.pagemax = 0
        self.re_name = re.compile("_([^_]*)(_voo|)$")
        self.re_page = re.compile("javascript:__doPostBack\('grd_voos','Page\$([0-9]+)'\)")

    def handle_starttag(self, tag, attrs):
        self.openspan = ''
        if (tag == 'span'):
            dic = dict(attrs)
            if (dic.has_key('id')):
                if (dic.get('id').startswith('grd_voos_ctl') or (dic.get('id') == 'lbl_data_pagedate')):
                    self.openspan = dic.get('id')

        elif (tag == 'tr'):
            dic = dict(attrs)
            if (dic.has_key('class')):
                if (dic.get('class') == 'pagina'):
                    self.openpagination = True

        elif (self.openpagination):
            if (tag == "a"):
                dic = dict(attrs)
                if (dic.has_key('href')):
                    page = self.re_page.search(dic.get('href'))
                    if (page != None):
                        page = int(page.group(1))
                        if (page > self.pagemax):
                            self.pagemax = page

    def handle_data(self, data):
        if (self.openspan == 'lbl_data_pagedate'):
            self.pagedate = data
        elif (self.openspan != ''):
            key = self.re_name.search(self.openspan).group(1).lower()
            self.flightdata.append(tuple([key,data]))
            if (self.openspan.startswith('grd_voos_ctl') and self.openspan.endswith('STATUS')):
                self.flights.append(self.flightdata)
                self.flightdata = []
        if (self.openspan != ''):
            self.openspan = ''

    def get_flights(self):
        return self.flights
    
    def get_date(self):
        return self.pagedate
    
    def get_pages(self):
        return self.pagemax

class Harvester:
    def __init__(self):
        cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        self.pagedate = ''
        self.pagemax = 0
        self.requestvars = []

    def get_date(self):
        return self.pagedate

    def get_pages(self):
        return self.pagemax

    def request_session_page(self,url):
        request = self.opener.open(url,urllib.urlencode(self.requestvars))
        data = request.read()
        parser = RequestVarsHTMLParser()
        parser.feed(data)
        parser.close()
        self.requestvars = parser.get_request_vars()

    def request_start(self):
        self.pagedate = ''
        self.request_session_page('http://www.infraero.gov.br/voos/index.aspx')

    def request_intermediate(self, target):
        manager = 'update|' + target
        self.request_start()
        self.requestvars.append(tuple(['ScriptManager1', manager]))
        self.requestvars.append(tuple(['__EVENTTARGET', target]))
        self.requestvars.append(tuple(['__EVENTARGUMENT', '']))
        self.requestvars.append(tuple(['opcoes', '0']))
        self.requestvars.append(tuple(['pode_pesquisar_aeroporto', 'S']))

        self.request_session_page('http://www.infraero.gov.br/voos/index.aspx')

    def request_data_page(self,url):
        request = self.opener.open(url,urllib.urlencode(self.requestvars))
        data = request.read()
        parser = RequestVarsHTMLParser()
        parser.feed(data)
        parser.close()
        self.requestvars = parser.get_request_vars()

        parser = FlightDataHTMLParser()
        parser.feed(data)
        parser.close()

        if (self.pagedate == ''):
            self.pagedate = parser.get_date()
        if (self.pagemax < parser.get_pages()):
            self.pagemax = parser.get_pages()

        return parser.get_flights()    

    def request_airport_pages(self, airport, page):
        argument = 'Page$' + str(page)
        self.requestvars.append(tuple(['ScriptManager1', 'update_grid|grd_voos']))
        self.requestvars.append(tuple(['__EVENTTARGET', 'grd_voos']))
        self.requestvars.append(tuple(['__EVENTARGUMENT', argument]))
        self.requestvars.append(tuple(['opcoes', '0']))
        self.requestvars.append(tuple(['dpl_aeroporto', airport]))
        self.requestvars.append(tuple(['txt_num_voo', '']))
        self.requestvars.append(tuple(['__LASTFOCUS', '']))

        return self.request_data_page('http://www.infraero.gov.br/voos/index_2.aspx')

    def request_flight(self, airport, flight):
        self.pagemax = 1

        flight = '' + str(flight)
        while (len(flight) < 5):
            flight = '0' + flight

        self.request_intermediate('hl_3')
        self.requestvars.append(tuple(['ScriptManager1', 'update|btn_aeroporto']))
        self.requestvars.append(tuple(['__EVENTTARGET', '']))
        self.requestvars.append(tuple(['__EVENTARGUMENT', '']))
        self.requestvars.append(tuple(['opcoes', '0']))
        self.requestvars.append(tuple(['pode_pesquisar_aeroporto', 'S']))
        self.requestvars.append(tuple(['aeroportos_chegada_1', airport]))
        self.requestvars.append(tuple(['txt_num_voo',flight]))
        self.requestvars.append(tuple(['txt_water_box_ClientState', '']))
        self.requestvars.append(tuple(['btn_aeroporto', "Consultar V\xc3\xb4os"]))

        return self.request_data_page('http://www.infraero.gov.br/voos/index.aspx')
    
    def request_airport(self, airport):
        self.pagemax = 1

        self.request_intermediate('hl_1')
        self.requestvars.append(tuple(['ScriptManager1', 'update|btn_aeroporto_3']))
        self.requestvars.append(tuple(['__EVENTTARGET', '']))
        self.requestvars.append(tuple(['__EVENTARGUMENT', '']))
        self.requestvars.append(tuple(['opcoes', '0']))
        self.requestvars.append(tuple(['pode_pesquisar_aeroporto', 'S']))
        self.requestvars.append(tuple(['aero_companias_1', airport]))
        self.requestvars.append(tuple(['btn_aeroporto_3', "Consultar V\xc3\xb4os"]))

        data = self.request_data_page('http://www.infraero.gov.br/voos/index.aspx')

        i = 1
        while (i < self.pagemax):
            i = i+1
            data = data + self.request_airport_pages(airport, i)

        return data

class Formater:
    def __init__(self, flights):
        self.flights = flights

    def print_table_row(self, flight, head):
        if (head == True):
            hd = 'h'
            index = 0
        else:
            hd = 'd'
            index = 1

        dic = dict(flight)
        color = 'black'
        if (dic.get('status').lower() == 'cancelado'):
            color = 'red'

        print '<tr>'
        for data in flight:
            print '<t' + hd + ' style="color: ' + color + '">'
            print data[index]
            print '</t' + hd + '>'
        print '</tr>'

    def print_table(self, id):
        first = True
        print '<table id="' + id + '">'
        for flight in self.flights:
            if first:
                print '<thead>'
                self.print_table_row(flight,True)
                print '</thead><tbody>'
                first = False
            self.print_table_row(flight,False)
        print '</tbody></table>'
