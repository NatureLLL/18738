// // Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['corechart']});
//
// // Set a callback to run when the Google Visualization API is loaded.
// google.charts.setOnLoadCallback(drawGoogleChart);

 var value = [0, 0, 0, 0];
function drawGoogleChart() {
    var data = new google.visualization.DataTable();
     data.addColumn('string','Location');
    data.addColumn('number','Area');
    data.addRows([
        ['area1', value[0]],
        ['area2', value[1]],
        ['area3', value[2]],
        ['area4', value[3]]
    ]);
    // Optional; add a title and set the width and height of the chart
    var options = {'title': 'Integral Hit Distribution', 'width': 1000, 'height': 800};

    // Display the chart inside the <div> element with id="piechart"
    var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
    chart.draw(data, options);

}


function update(data) {
    hit = [0, 0, 0, 0];
    for (var i = 0; i < data.records.length; i++) {
        var record = data.records[i];
        hit[0] += record['hit1'];
        hit[1] += record['hit2'];
        hit[2] += record['hit3'];
        hit[3] += record['hit4'];
    }
    for (var i = 0; i < 4; i++) {
        value[i] = hit[i];
    }
    google.charts.setOnLoadCallback(drawGoogleChart);
}


$(document).ready(function () {
    $.get("/grumblr/get_data").done(function (data) {
        update(data);
    });

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawGoogleChart);


console.log("here");
    $("#fake").on("click", function () {
        console.log("here");
        $.get('/grumblr/fake_data').done(function (data) {
            console.log("call fake");
            update(data);
        }).catch((a, b, c) => {
            console.log('err', a, b, c)
        });
    });

    $("#reset").on('click', function () {
        $.get("/grumblr/reset_data").done(function (data) {
            update(data);
        }).catch((a, b, c) => {
            console.log('err', a, b, c)
        });
    });
});