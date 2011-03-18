========
Tutorial
========

Using pycha is quite simple. You always follow the same 5 simple steps:

1. Create a Cairo surface to draw the chart on
2. Build a list of data sets from which your chart will be created
3. Customize the chart options.
4. Create the chart, add the datasets and render it
5. Save the results into a file or do whatever you want with the Cairo
   surface

To create the Cairo surface you just need to say the type of surface and its
dimensions::

   import cairo
   width, height = (500, 400)
   surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

Then you should create your data set querying a database or any other data
source::

   dataSet = (
     ('dataSet 1', ((0, 1), (1, 3), (2, 2.5))),
     ('dataSet 2', ((0, 2), (1, 4), (2, 3))),
     ('dataSet 3', ((0, 5), (1, 1), (2, 0.5))),
   )

As you can see, each data set is a tuple where the first element is the name of
the data set and the second is another tuple composed by points. Each point is a
two-elements tuple, the first one is the x value and the second the y value.

Not every chart uses all the information of a data set. For example, the Pie
chart only uses the first point of each dataset and it only uses the y value of
the point.

Now you may want to specify some options so the chart can be customize changing
its defaults values. To see the defaults you can check the
pycha.chart.Chart.__init__ method in the source code. You can use regular
dictionaries to define your options. For example, imagine you want to hide the
legend and use a different color for the background::

   options = {
       'legend': {'hide': True},
       'background': {'color': '#f0f0f0'},
   }

Now we are ready to instantiate the chart, add the data set and render it::

   import pycha.bar
   chart = pycha.bar.VerticalBarChart(surface, options)
   chart.addDataset(dataSet)
   chart.render()


Right now you can choose among several different kind of charts:

* Pie Charts (``pycha.pie.PieChart``)
* Bar Charts (``pycha.bar.VerticalBarChart`` and
  ``pycha.bar.HorizontalBarChart``)
* Line Charts (``pycha.bar.LineChart``)
* Scatterplot Charts (``pycha.scatter.ScatterplotChart``)
* Stacked Bar Charts (``pycha.stackedbar.StackedVerticalBarChart`` and
  ``pycha.stackedbar.StackedHorizontalBarChart``)

Finally you can write the surface to a graphic file or anything you want using
the cairo library::

   surface.write_to_png('output.png')

That's it!
