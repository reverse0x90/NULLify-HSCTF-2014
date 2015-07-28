	function getJSON()
	{
		var retVal;
		$.ajax({ // create an AJAX call...
        type: 'GET', // GET or POST
        url: '/scores/', // the file to call
		async: false,
        success: function(response) { // on success..
             retVal = response;
        }
		});
		
		return JSON.parse(retVal);
	}
	
function getScores() {
	
	var Results = getJSON();
	
   $(function () {
        $('#scoreboard').highcharts({
            chart: {
                type: 'bar'
            },
            title: {
                text: 'Current Scoreboard'
            },
            xAxis: {
                categories: Results.teams,
                title: {
                    text: null
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Points',
                    align: 'high'
                },
                labels: {
                    overflow: 'justify'
                }
            },
            tooltip: {
                valueSuffix: ' points'
            },
            plotOptions: {
                bar: {
                    dataLabels: {
                        enabled: true
                    }
                },
				series: {
                cursor: 'pointer',
                point: {
                    events: {
                        click: function () {
                            location.href = this.options.url;
                        }
                    }
                }
				}
            },
            credits: {
                enabled: false
            },
            series: [{
				name: 'Current Points',
				color: 'black',
                data: Results.scores,
				showInLegend:false
            }]
        });
    });
   // and schedule a repeat
   setTimeout(getScores, 60000);
}

// start the cycle
getScores();