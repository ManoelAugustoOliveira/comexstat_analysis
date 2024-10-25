def ApexBarChart(x_values, y_values, x_title, y_title, orientation='vertical', bar_color='#1E90FF', value_unit='U$'):
    is_horizontal = orientation == 'horizontal'

    if value_unit == 'KG':
        y_formatter = "function(val) { return val.toFixed(0) + ' KG'; }"
        tooltip_formatter = "function(val) { return val.toLocaleString('pt-BR') + ' KG'; }"
    elif value_unit == 'U$':
        y_formatter = "function(val) { return val.toLocaleString('pt-BR', { style: 'currency', currency: 'USD' }); }"
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
                plotOptions: {{
                    bar: {{
                        borderRadius: 5,
                        horizontal: {str(is_horizontal).lower()},
                        columnWidth: '50%'
                    }}
                }},
                colors: ['{bar_color}'],
                dataLabels: {{
                    enabled: false
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
                        formatter: {y_formatter},
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