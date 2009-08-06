#!/usr/bin/python2.5
#
# Copyright 2008 the Melange authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Set of known *current* country and territory names.

Legacy (duplicate) names for some countries have been removed from the
original list.  Also missing are the following U.S. OFAC embargoed and
Commerce Department export-controlled countries:

  Cuba, Iran, Myanmar (formerly Burma), North Korea, Sudan, Syria
"""

__authors__ = [
  '"Daniel Hans" <daniel.m.hans@gmail.com>',
  '"Madhusudan.C.S" <madhusudancs@gmail.com>',
  '"Todd Larsen" <tlarsen@google.com>',
]

COUNTRY_INFO = {
    "Afghanistan, Islamic State of": ('.af', 'Asia'),
    "Albania": ('.al', 'Europe'),
    "Algeria": ('.dz', 'Africa'),
    "American Samoa": ('.as', 'Australia'),
    "Andorra, Principality of": ('.ad', 'Europe'),
    "Angola": ('.ao', 'Africa'),
    "Anguilla": ('.ai', 'North America'),
    "Antarctica": ('.aq', 'Europe'),
    "Antigua and Barbuda": ('.ag', 'North America'),
    "Argentina": ('.ar', 'South America'),
    "Armenia": ('.am', 'Asia'),
    "Aruba": ('.aw', 'North America'),
    "Australia": ('.au', 'Australia'),
    "Austria": ('.at', 'Europe'),
    "Azerbaidjan": ('.az', 'Asia'),
    "Bahamas": ('.bs', 'North America'),
    "Bahrain": ('.bh', 'Asia'),
    "Bangladesh": ('.bd', 'Asia'),
    "Barbados": ('.bb', 'North America'),
    "Belarus": ('.by', 'Europe'),
    "Belgium": ('.be', 'Europe'),
    "Belize": ('.bz', 'North America'),
    "Benin": ('.bj', 'Africa'),
    "Bermuda": ('.bm', 'North America'),
    "Bhutan": ('.bt', 'Asia'),
    "Bolivia": ('.bo', 'South America'),
    "Bosnia-Herzegovina": ('.ba', 'Europe'),
    "Botswana": ('.bw', 'Africa'),
    "Bouvet Island": ('.bv', 'Europe'),
    "Brazil": ('.br', 'South America'),
    "British Indian Ocean Territory": ('.io', 'Asia'),
    "Brunei Darussalam": ('.bn', 'Asia'),
    "Bulgaria": ('', 'Europe'),
    "Burkina Faso": ('.bg', 'Africa'),
    "Burundi": ('.bi', 'Africa'),
    "Cambodia, Kingdom of": ('.kh', 'Asia'),
    "Cameroon": ('.cm', 'Africa'),
    "Canada": ('.ca', 'North America'),
    "Cape Verde": ('.cv', 'Africa'),
    "Cayman Islands": ('.ky', 'North America'),
    "Central African Republic": ('.cf', 'Africa'),
    "Chad": ('.td', 'Africa'),
    "Chile": ('.cl', 'South America'),
    "China": ('.cn', 'Asia'),
    "Christmas Island": ('.cx', 'Australia'),
    "Cocos (Keeling) Islands": ('.cc', 'Australia'),
    "Colombia": ('.co', 'South America'),
    "Comoros": ('.km', 'Africa'),
    "Congo": ('.cg', 'Africa'),
    "Congo, Democratic Republic of the": ('.cd', 'Africa'),
    "Cook Islands": ('.ck', 'Australia'),
    "Costa Rica": ('.cr', 'North America'),
    "Croatia": ('.hr', 'Europe'),
    "Cyprus": ('.cy', 'Asia'),
    "Czech Republic": ('.cz', 'Europe'),
    "Denmark": ('.dk', 'Europe'),
    "Djibouti": ('.dj', 'Africa'),
    "Dominica": ('.dm', 'North America'),
    "Dominican Republic": ('.do', 'North America'),
    "East Timor": ('.tl', 'Asia'),
    "Ecuador": ('.ec', 'South America'),
    "Egypt": ('.eg', 'Africa'),
    "El Salvador": ('.sv', 'North America'),
    "Equatorial Guinea": ('.gq', 'Africa'),
    "Eritrea": ('.er', 'Africa'),
    "Estonia": ('.ee', 'Europe'),
    "Ethiopia": ('.et', 'Africa'),
    "Falkland Islands": ('.fk', 'South America'),
    "Faroe Islands": ('.fo', 'Europe'),
    "Fiji": ('.fj', 'Australia'),
    "Finland": ('.fi', 'Europe'),
    "France": ('.fr', 'Europe'),
    "French Guyana": ('.gf', 'South America'),
    "French Southern Territories": ('.tf', 'Africa'),
    "Gabon": ('.ga', 'Africa'),
    "Gambia": ('.gm', 'Africa'),
    "Georgia": ('.ge', 'Asia'),
    "Germany": ('.de', 'Europe'),
    "Ghana": ('.gh', 'Africa'),
    "Gibraltar": ('.gi', 'Europe'),
    "Greece": ('.gr', 'Europe'),
    "Greenland": ('.gl', 'North America'),
    "Grenada": ('.gd', 'North America'),
    "Guadeloupe (French)": ('.gp', 'North America'),
    "Guam (USA)": ('.gu', 'Australia'),
    "Guatemala": ('.gt', 'North America'),
    "Guinea": ('.gn', 'Africa'),
    "Guinea Bissau": ('.gw', 'Africa'),
    "Guyana": ('.gy', 'South America'),
    "Haiti": ('.ht', 'North America'),
    "Heard and McDonald Islands": ('.hm', 'Australia'),
    "Holy See (Vatican City State)": ('.va', 'Europe'),
    "Honduras": ('.hn', 'North America'),
    "Hong Kong": ('.hk', 'Asia'),
    "Hungary": ('.hu', 'Europe'),
    "Iceland": ('.is', 'Europe'),
    "India": ('.in', 'Asia'),
    "Indonesia": ('.id', 'Asia'),
    "Iraq": ('.iq', 'Asia'),
    "Ireland": ('.ie', 'Europe'),
    "Israel": ('.il', 'Asia'),
    "Italy": ('.it', 'Europe'),
    "Ivory Coast": ('.ci', 'Africa'),
    "Jamaica": ('.jm', 'North America'),
    "Japan": ('.jp', 'Asia'),
    "Jordan": ('.jo', 'Asia'),
    "Kazakhstan": ('.kz', 'Asia'),
    "Kenya": ('.ke', 'Africa'),
    "Kiribati": ('.ki', 'Australia'),
    "Kuwait": ('.kw', 'Asia'),
    "Kyrgyz Republic (Kyrgyzstan)": ('.kg', 'Asia'),
    "Laos": ('.la', 'Asia'),
    "Latvia": ('.lv', 'Europe'),
    "Lebanon": ('.lb', 'Asia'),
    "Lesotho": ('.ls', 'Africa'),
    "Liberia": ('.lr', 'Africa'),
    "Libya": ('.ly', 'Africa'),
    "Liechtenstein": ('.li', 'Europe'),
    "Lithuania": ('.lt', 'Europe'),
    "Luxembourg": ('.lu', 'Europe'),
    "Macau": ('.mo', 'Asia'),
    "Macedonia": ('.mk', 'Europe'),
    "Madagascar": ('.mg', 'Africa'),
    "Malawi": ('.mw', 'Africa'),
    "Malaysia": ('.my', 'Asia'),
    "Maldives": ('.mv', 'Asia'),
    "Mali": ('.ml', 'Africa'),
    "Malta": ('.mt', 'Europe'),
    "Marshall Islands": ('.mh', 'Australia'),
    "Martinique (French)": ('.mq', 'North America'),
    "Mauritania": ('.mr', 'Africa'),
    "Mauritius": ('.mu', 'Africa'),
    "Mayotte": ('.yt', 'Africa'),
    "Mexico": ('.mx', 'North America'),
    "Micronesia": ('.fm', 'Australia'),
    "Moldavia": ('.md', 'Europe'),
    "Monaco": ('.mc', 'Europe'),
    "Mongolia": ('.mn', 'Asia'),
    "Montenegro": ('.me', 'Europe'),
    "Montserrat": ('.ms', 'North America'),
    "Morocco": ('.ma', 'Africa'),
    "Mozambique": ('.mz', 'Africa'),
    "Namibia": ('.na', 'Africa'),
    "Nauru": ('.nr', 'Australia'),
    "Nepal": ('.np', 'Asia'),
    "Netherlands": ('.nl', 'Europe'),
    "Netherlands Antilles": ('.an', 'North America'),
    "New Caledonia (French)": ('.nc', 'Australia'),
    "New Zealand": ('.nz', 'Australia'),
    "Nicaragua": ('.ni', 'North America'),
    "Niger": ('.ne', 'Africa'),
    "Nigeria": ('.ng', 'Africa'),
    "Niue": ('.nu', 'Australia'),
    "Northern Mariana Islands": ('.mp', 'Australia'),
    "Norway": ('.no', 'Europe'),
    "Oman": ('.om', 'Asia'),
    "Pakistan": ('.pk', 'Asia'),
    "Palau": ('.pw', 'Australia'),
    "Palestinian Territories": ('.ps', 'Asia'),
    "Panama": ('.pa', 'North America'),
    "Papua New Guinea": ('.pg', 'Australia'),
    "Paraguay": ('.py', 'South America'),
    "Peru": ('.pe', 'South America'),
    "Philippines": ('.ph', 'Asia'),
    "Pitcairn Island": ('.pn', 'South America'),
    "Poland": ('.pl', 'Europe'),
    "Polynesia (French)": ('.pf', 'Australia'),
    "Portugal": ('.pt', 'Europe'),
    "Puerto Rico": ('.pr', 'North America'),
    "Qatar": ('.qa', 'Asia'),
    "Reunion (French)": ('.re', 'Africa'),
    "Romania": ('.ro', 'Europe'),
    "Russian Federation": ('.ru', 'Europe'),
    "Rwanda": ('.rw', 'Africa'),
    "South Georgia & South Sandwich Islands": ('.gs', 'South America'),
    "Saint Helena": ('.sh', 'Africa'),
    "Saint Kitts & Nevis Anguilla": ('.kn', 'North America'),
    "Saint Lucia": ('.lc', 'North America'),
    "Saint Pierre and Miquelon": ('.pm', 'North America'),
    "Saint Tome (Sao Tome) and Principe": ('.st', 'Africa'),
    "Saint Vincent & Grenadines": ('.vc', 'North America'),
    "Samoa": ('.ws', 'Australia'),
    "San Marino": ('.sm', 'Europe'),
    "Saudi Arabia": ('.sa', 'Asia'),
    "Senegal": ('.sn', 'Africa'),
    "Serbia": ('.rs', 'Europe'),
    "Seychelles": ('.sc', 'Africa'),
    "Sierra Leone": ('.sl', 'Africa'),
    "Singapore": ('.sg', 'Asia'),
    "Slovak Republic": ('.sk', 'Europe'),
    "Slovenia": ('.si', 'Europe'),
    "Solomon Islands": ('.sb', 'Australia'),
    "Somalia": ('.so', 'Africa'),
    "South Africa": ('.za', 'Africa'),
    "South Korea": ('.kr', 'Asia'),
    "Spain": ('.es', 'Europe'),
    "Sri Lanka": ('.lk', 'Asia'),
    "Suriname": ('.sr', 'South America'),
    "Svalbard and Jan Mayen Islands": ('.sj', 'Europe'),
    "Swaziland": ('.sz', 'Africa'),
    "Sweden": ('.se', 'Europe'),
    "Switzerland": ('.ch', 'Europe'),
    "Tadjikistan": ('.tj', 'Asia'),
    "Taiwan": ('.tw', 'Asia'),
    "Tanzania": ('.tz', 'Africa'),
    "Thailand": ('.th', 'Asia'),
    "Togo": ('.tg', 'Africa'),
    "Tokelau": ('.tk', 'Australia'),
    "Tonga": ('.to', 'Australia'),
    "Trinidad and Tobago": ('.tt', 'North America'),
    "Tunisia": ('.tn', 'Africa'),
    "Turkey": ('.tr', 'Asia'),
    "Turkmenistan": ('.tm', 'Asia'),
    "Turks and Caicos Islands": ('.tc', 'North America'),
    "Tuvalu": ('.tv', 'Australia'),
    "USA Minor Outlying Islands": ('.um', 'North America'),
    "Uganda": ('.ug', 'Africa'),
    "Ukraine": ('.ua', 'Europe'),
    "United Arab Emirates": ('.ae', 'Asia'),
    "United Kingdom": ('.uk', 'Europe'),
    "United States": ('.us', 'North America'),
    "Uruguay": ('.uy', 'South America'),
    "Uzbekistan": ('.uz', 'Asia'),
    "Vanuatu": ('.vu', 'Australia'),
    "Venezuela": ('.ve', 'South America'),
    "Vietnam": ('.vn', 'Asia'),
    "Virgin Islands (British)": ('.vg', 'North America'),
    "Virgin Islands (USA)": ('.vi', 'North America'),
    "Wallis and Futuna Islands": ('.wf', 'Australia'),
    "Western Sahara": ('.eh', 'Africa'),
    "Yemen": ('.ye', 'Asia'),
    "Zambia": ('.zm', 'Africa'),
    "Zimbabwe": ('.zw', 'Africa'),
    }

# List of all countries and territories
COUNTRIES_AND_TERRITORIES = COUNTRY_INFO.keys() 

# Mapping of countries to their CCTLD
COUNTRIES_TO_CCTLD = dict((k, c) for k, (c, _) in COUNTRY_INFO.items()) 

# Mapping of countries to their continent
COUNTRIES_TO_CONTINENT = dict((k, c) for k, (_, c) in COUNTRY_INFO.items())
