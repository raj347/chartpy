__author__ = 'saeedamen' # Saeed Amen

#
# Copyright 2016 Cuemacro
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and limitations under the License.
#

"""
Chart

Creates chart using several underlying plotting libraries (Matplotlib, Plotly and Bokeh) using the same interface

"""

from chartpy.twitter import Twitter
from chartpy.chartconstants import ChartConstants
from chartpy.style import Style
from chartpy.engine import EngineMatplotlib, EngineBokeh, EnginePlotly

class Chart(object):

    df = None
    engine = ChartConstants().chartfactory_default_engine
    style = Style()
    chart_type = 'line' # default chart type is line chart

    def __init__(self, df = None, engine = None, chart_type = None, style = None):

        if df is not None: self.df = df
        if engine is not None: self.engine = engine
        if chart_type is not None: self.chart_type = chart_type
        if style is not None: self.style = style

        pass

    ##### implemented chart types:
    ##### heatmap (Plotly)
    ##### line (Bokeh, Matplotlib, Plotly)
    ##### bar (Bokeh, Matplotlib, Plotly)
    ##### stacked (Bokeh, Matplotlib, Plotly)
    ##### surface (Plotly)
    def plot(self, df = None, engine = None, chart_type = None, style = None, twitter_msg = None, twitter_on = False):

        if style is None: style = self.style
        if df is None: df = self.df

        if engine is None:
            try:
                engine = style.engine
            except:
                engine = self.engine

        if chart_type is None:
            chart_type = self.chart_type

            try:
                if style.chart_type is not None:
                    chart_type = style.chart_type
            except:
                pass

        fig = self.get_engine(engine).plot_chart(df, style, chart_type)

        if twitter_on:
            twitter = Twitter()
            twitter.auto_set_key()
            twitter.update_status(twitter_msg, picture=style.file_output)

        return fig

    def get_engine(self, engine):

        if engine is None:          return self.get_engine(self.engine)
        elif engine == 'matplotlib':  return EngineMatplotlib()
        elif engine == 'bokeh':     return EngineBokeh()
        elif engine == 'plotly':    return EnginePlotly()

        return None

    def _iplot(self, data_frame, engine=engine, chart_type=None, style=None):
        return Chart.get_engine(engine).plot_chart(data_frame, style, chart_type)

#######################################################################################################################

