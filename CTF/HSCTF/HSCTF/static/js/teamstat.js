var pathArray = window.location.pathname.split( '/' );
var team = decodeURIComponent(pathArray[pathArray.length - 2]);
	
function getScoresJSON()
{
	var retVal;
	$.ajax({ // create an AJAX call...
	type: 'GET', // GET or POST
	url: '/tscores/'+team+'/', // the file to call
	async: false,
	success: function(response) { // on success..
		 retVal = response;
	}
	});
	
	return JSON.parse(retVal);
}

function getSubmissionsJSON()
{
	var retVal;
	$.ajax({ // create an AJAX call...
	type: 'GET', // GET or POST
	url: '/tpoints/'+team+'/', // the file to call
	async: false,
	success: function(response) { // on success..
		 retVal = response;
	}
	});
	
	return JSON.parse(retVal);
}
	
function getTeamScores() {
	
	var Results = getScoresJSON();
	$(function () {
    $('#team').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: 1,//null,
            plotShadow: false
        },
        title: {
            text: 'Points Breakdown'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.y:.0f} Points', 
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            type: 'pie',
            name: 'Percentage Team Points: ',
            data: [
                ['Recon', Results.recon],
                ['Trivia', Results.trivia],
                ['Script', Results.script],
                ['Web', Results.web],
				['Binary', Results.binary],
				['Crypto', Results.crypto],
				['Stego/Forensics', Results.stego],
				['Network', Results.network],
				['Grab Bag', Results.grab_bag],
				['Flash', Results.flash]	
            ]
        }]
    });
});

}

function getTeamSubmissions() {
	var Results = getSubmissionsJSON();
	$(function() {
		Highcharts.setOptions({colors: ['#00B200','#FF0000']});
        // Create the chart
        $('#submissions').highcharts({
            chart: {
                plotBackgroundColor: null,
				plotBorderWidth: 1,//null,
                type: 'pie'
            },
            title: {
                text: 'Flag Submissions'
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.0f}%', 
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
			},
            tooltip: {
            pointFormat: '{series.name}: <b>{point.y:.0f}</b>' 
			},
            series: [{
                name: 'Submissions',
                data: [["Correct Flags",Results.correct_flags],["Wrong Flags",Results.wrong_flags]],
                size: '70%',
                innerSize: '40%',
                showInLegend:false,
                dataLabels: {
                    enabled: true
                }
            }]
        });
    });

}

// start the cycle
getTeamScores();
getTeamSubmissions();
