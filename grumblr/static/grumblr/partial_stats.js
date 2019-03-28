// // Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['line']});
//
// // Set a callback to run when the Google Visualization API is loaded.
// google.charts.setOnLoadCallback(drawGoogleChart);

 var global_records;

function drawIndivChart() {
    var data = new google.visualization.DataTable();
      data.addColumn('number', 'Time');
      data.addColumn('number', 'Area1');
      data.addColumn('number', 'Area2');
      data.addColumn('number', 'Area3');
      data.addColumn('number', 'Area4');
      for (var i = 0; i < global_records.length; i++) {
          var record = global_records[i];
          data.addRow([i, record['hit1'], record['hit2'], record['hit3'], record['hit4'],]);
      }
      var options = {
        chart: {
          title: 'Number of Hit in Different Area ',
        },
        width: 900,
        height: 500
      };

      var chart = new google.charts.Line(document.getElementById('indiv_chart_div'));

      chart.draw(data, google.charts.Line.convertOptions(options));
}

$(document).ready(function () {
// Set a callback to run when the Google Visualization API is loaded.
    $.get("/grumblr/get_data").done(function (data) {
        global_records = data.records;
    });
google.charts.setOnLoadCallback(drawIndivChart);

});