# Copyright 2010 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Class used for determining GeoIP location."""

import re
import tempfile

# external dependencies (from nb_third_party)
import httplib2
import simplejson

import util


def GetFromTelizeJSAPI():
  h = httplib2.Http(tempfile.gettempdir(), timeout=10)
  unused_resp, content = h.request('http://www.telize.com/geoip', 'GET')
  data = simplejson.loads(content)
  return {
		'region_name': data.get('region'),
		'country_name': data.get('country'),
		'country_code': data.get('country_code'),
		'city': data.get('city'),
		'latitude': data.get('latitude'),
		'longitude': data.get('longitude'),
		'source': 'mmind'
  }


def GetGeoData():
  """Get geodata from any means necessary. Sanitize as necessary."""
  try:
    json_data = GetFromTelizeJSAPI()

    # Make our data less accurate. We don't need any more than that.
    json_data['latitude'] = '%.3f' % float(json_data['latitude'])
    json_data['longitude'] = '%.3f' % float(json_data['longitude'])
    return json_data
  except:
    print 'Failed to get Geodata: %s' % util.GetLastExceptionString()
    return {}
