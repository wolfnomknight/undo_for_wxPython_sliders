# Undo function for wx sliders
# By Wolfnom ~ Sergio Augusto Knapik - 2022

import wx
import wx.xrc

app = wx.App()


class UndoInterface(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Undo Function for Sliders", pos=wx.DefaultPosition,
                          size=wx.Size(300, 240), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        # The following parts are the building of a simple GUI with 4 sliders to show the effect of the code

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        sizer1 = wx.FlexGridSizer(3, 2, 0, 0)
        sizer1.SetFlexibleDirection(wx.BOTH)
        sizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_NONE)

        # Title
        self.title = wx.StaticText(self, id=wx.ID_ANY, label="Undo Function for wx Sliders",
                                   pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.title.Wrap(-1)
        self.title.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), family=wx.FONTFAMILY_DEFAULT,
                                   style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL))

        sizer1.Add(self.title, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.EXPAND, border=4)

        sizer1.Add((0, 0), proportion=1, flag=wx.EXPAND, border=4)

        sizer2 = wx.FlexGridSizer(2, 0, 0, 0)
        sizer2.SetFlexibleDirection(wx.BOTH)
        sizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # First slider
        self.slider1 = wx.Slider(self, id=wx.ID_ANY, value=0, minValue=-10, maxValue=10,
                                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                                 style=wx.SL_HORIZONTAL | wx.SL_LABELS, name="slider1")
        sizer2.Add(self.slider1, proportion=0, flag=wx.ALL, border=4)
        # This bind uses EVT_LEFT_UP, that checks when the user releases the mouse button
        # and calls the function to storage the change for the undo
        # To call another function it's possible to bind the slider again
        # using EVT_SLIDER to get a real-time value or call the other
        # function inside the handler
        self.slider1.Bind(event=wx.EVT_LEFT_UP, handler=self.slider1_function)

        # Second slider
        self.slider2 = wx.Slider(self, id=wx.ID_ANY, value=0, minValue=-20, masxValue=20,
                                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                                 style=wx.SL_HORIZONTAL | wx.SL_INVERSE | wx.SL_LABELS, name="slider2")
        sizer2.Add(self.slider2, proportion=0, flag=wx.ALL, border=4)
        self.slider2.Bind(event=wx.EVT_LEFT_UP, handler=self.slider2_function)

        sizer1.Add(sizer2, proportion=1, flag=wx.ALL | wx.EXPAND, border=4)

        sizer3 = wx.FlexGridSizer(0, 2, 0, 0)
        sizer3.SetFlexibleDirection(wx.BOTH)
        sizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # Third slider
        self.vertical_slider3 = wx.Slider(self, id=wx.ID_ANY, value=50, minValue=0, maxValue=100,
                                          pos=wx.DefaultPosition, size=wx.DefaultSize,
                                          style=wx.SL_LABELS | wx.SL_VERTICAL, name="slider4")
        sizer3.Add(self.vertical_slider3, proportion=0, flag=wx.ALL, border=4)
        self.vertical_slider3.Bind(event=wx.EVT_LEFT_UP, handler=self.slider4_function)

        # Forth slider
        self.vertical_slider4 = wx.Slider(self, id=wx.ID_ANY, value=50, minValue=0, maxValue=100,
                                          pos=wx.DefaultPosition, size=wx.DefaultSize,
                                          style=wx.SL_LABELS | wx.SL_VALUE_LABEL | wx.SL_VERTICAL, name="slider3")
        sizer3.Add(self.vertical_slider4, proportion=0, flag=wx.ALL, border=4)
        self.vertical_slider4.Bind(event=wx.EVT_LEFT_UP, handler=self.slider3_function)

        sizer1.Add(sizer3, proportion=1, flag=wx.ALL | wx.EXPAND, border=4)

        # Undo button
        self.undo_button = wx.Button(self, id=wx.ID_ANY, label="Undo", pos=wx.DefaultPosition,
                                     size=wx.DefaultSize, style=0)
        sizer1.Add(self.undo_button, proportion=0, flag=wx.ALL | wx.EXPAND, border=4)
        self.undo_button.Bind(event=wx.EVT_BUTTON, handler=self.undo_function)

        # Close button
        self.close_button = wx.Button(self, id=wx.ID_ANY, label="Close", pos=wx.DefaultPosition,
                                      size=wx.DefaultSize, style=0)
        sizer1.Add(self.close_button, proportion=0, flag=wx.ALL | wx.EXPAND, border=4)
        self.close_button.Bind(event=wx.EVT_BUTTON, handler=self.close_function)

        # Finally the logic behind the "undo"

        # This list storages the actions taken by the user
        self.undo_list = list()

        # Dictionary with the sliders and their current values
        self.dict_of_sliders = {"slider1": 0,
                                "slider2": 0,
                                "slider3": 0,
                                "slider4": 0,
                                }

        # List of sliders to facilitate access later on
        self.list_of_sliders = [self.slider1, self.slider2, self.vertical_slider4, self.vertical_slider3]

        # Update dictionary values before showing the app window
        self.check_dict()

        self.SetSizer(sizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        self.Show(True)

        app.MainLoop()

    def close_function(self, event=None):
        # I don't think I have to explain anything here
        self.Close()

    def check_dict(self):
        # Function to update the entire slider dictionary
        # Checks if each dict item has the same name as a slider
        # and if it does, stores the slider current value in the
        # corresponding item in the dict.
        # Used to check the initial value of the sliders, as
        # the app might be reading info from somewhere.
        for dict_slider in self.dict_of_sliders:
            for list_slider in self.list_of_sliders:
                if dict_slider == list_slider.GetName():
                    self.dict_of_sliders[dict_slider] = list_slider.GetValue()
                    print(f"{dict_slider}: {self.dict_of_sliders[dict_slider]}")

        # When calling a handler, wx passes the 'event' parameter so the
        # function must have it or we'll get the 'too many arguments' error
    def slider1_function(self, event=None):
        # It's necessary to skip the event because the slider
        # have a built-in EVT_LEFT_UP. As we're calling it, we
        # also have to end it or the slider will lock into
        # the cursor.
        event.Skip()
        # Everytime the slider is moved and the mouse button is released,
        # the moved slider and its PREVIOUS value are stored in the undo list
        # The previous value comes from the slider dictionary
        self.undo_list.append([self.slider1, self.dict_of_sliders["slider1"]])
        # After storing the slider and the value, update the dictionary
        self.dict_of_sliders["slider1"] = self.slider1.GetValue()

        # The handler in the bind of the slider cannot contain
        # parameters when calling the function, so we have to
        # use a function for each slider
    def slider2_function(self, event=None):
        event.Skip()
        self.undo_list.append([self.slider2, self.dict_of_sliders["slider2"]])
        self.dict_of_sliders["slider2"] = self.slider2.GetValue()

    def slider3_function(self, event=None):
        event.Skip()
        self.undo_list.append([self.vertical_slider4, self.dict_of_sliders["slider3"]])
        self.dict_of_sliders["slider3"] = self.vertical_slider4.GetValue()

    def slider4_function(self, event=None):
        event.Skip()
        self.undo_list.append([self.vertical_slider3, self.dict_of_sliders["slider4"]])
        self.dict_of_sliders["slider4"] = self.vertical_slider3.GetValue()

    def undo_function(self, event=None):
        # Only activates the undo if there is something to be undone
        if len(self.undo_list) > 0:
            # Get which slider will receive the undo (the last item in the undo list)
            undo_slider = self.undo_list[-1][0]
            # Get the value the slider will be brought back to
            undo_value = self.undo_list[-1][1]
            # Set the slider to it's previous value
            undo_slider.SetValue(undo_value)
            # Delete the command from the undo list
            self.undo_list.pop(-1)
            # Update the slider dictionary
            self.dict_of_sliders[undo_slider.GetName()] = undo_value


UndoInterface(None)
