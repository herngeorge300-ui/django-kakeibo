var COLORS = [
    '#4dc9f6',
    '#f67019',
    '#f53794',
    '#537bc4',
    '#acc236',
    '#166a8f',
    '#00a950',
    '#58595b',
    '#8549ba',
]

var ctx = document.getElementById("myChart2");
var myLineChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels:[{% for d in category2 %}
            '{{ d }}',
            {% endfor %}],
        datasets:[
            {
                data:[{% for i in money2 %}
            '{{ i }}',
            {% endfor %}],
                backgroundColor: COLORS,
            },
        ],
    },
    options: {
        title: {
            display:true,
            text: '家計簿収入データ'
        }
    }
})
