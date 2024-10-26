def ApexBarChart(x_values, y_values, x_title, y_title, bar_color='#1E90FF', value_unit='U$'):

    if value_unit == 'KG':
        value_formatter = "function(val) { return Intl.NumberFormat('pt-BR', { notation: 'compact', compactDisplay: 'short' }).format(val) + ' KG'; }"
        tooltip_formatter = "function(val) { return val.toLocaleString('pt-BR') + ' KG'; }"
    elif value_unit == 'U$':
        value_formatter = "function(val) { return Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'USD', notation: 'compact', compactDisplay: 'short' }).format(val); }"
        tooltip_formatter = "function(val) { return val.toLocaleString('pt-BR', { style: 'currency', currency: 'USD' }); }"
    else:
        raise ValueError("Invalid value_unit. Use 'KG' or 'U$'.")
    
    apex_chart = f"""
        <div id="chart"></div>
        <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
        <script>
            var options = {{
                chart: {{
                    type: 'bar',
                    height: 350,
                    toolbar: {{
                        show: true
                    }},
                }},
                series: [{{
                    name: 'Valores',
                    data: {y_values}
                }}],
                plotOptions: {{
                    bar: {{
                        borderRadius: 5,
                        columnWidth: '60%'
                    }}
                }},
                colors: ['{bar_color}'],
                dataLabels: {{
                    enabled: false
                }},
                xaxis: {{
                    categories: {x_values},
                    title: {{
                        text: '{x_title}',
                        style: {{
                            fontSize: '14px',
                            fontWeight: 'bold'
                        }}
                    }},
                    labels: {{
                        style: {{
                            fontSize: '12px',
                            colors: ['#333']
                        }}
                    }}
                }},
                yaxis: {{
                    title: {{
                        text: '{y_title}',
                        style: {{
                            fontSize: '14px',
                            fontWeight: 'bold'
                        }}
                    }},
                    labels: {{
                        formatter: {value_formatter},
                        style: {{
                            fontSize: '10px',
                            colors: ["#666"]
                        }}
                    }},
                    axisBorder: {{
                        show: false
                    }},
                    axisTicks: {{
                        show: false
                    }}
                }},
                tooltip: {{
                    enabled: true,
                    y: {{
                        formatter: {tooltip_formatter}
                    }}
                }},
                grid: {{
                    show: true,
                    borderColor: '#e0e0e0',
                    strokeDashArray: 4
                }}
            }};
            var chart = new ApexCharts(document.querySelector("#chart"), options);
            chart.render();
        </script>
    """
    
    return apex_chart
