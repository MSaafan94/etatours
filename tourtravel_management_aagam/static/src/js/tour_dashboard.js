/** @odoo-module **/
const { DateTime } = luxon;
import { serializeDate } from "@web/core/l10n/dates";

import {
    registry
} from "@web/core/registry";
import {
    useService
} from "@web/core/utils/hooks";
import {
    Component,
    EventBus,
    onWillStart,
    useSubEnv,
    useState,
    onMounted,
    onPatched
} from "@odoo/owl";
import {
    renderToElement
} from "@web/core/utils/render";

export class TourDashboard extends Component {
    init() {
        this._super.apply(this, arguments);
        this.rpc = this.bindService("rpc");
    }
    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");

        this.variants = [];
        this.warehouses = [];
        this.showVariants = false;
        this.uomName = "";
        this.extraColumnCount = 0;
        this.unfoldedIds = new Set();
        this.state = useState({
            showOptions: {
                uom: false,
                availabilities: false || Boolean(this.props.action.context.activate_availabilities),
                costs: true,
                operations: true,
                leadTimes: true,
                attachments: false,
            },
            currentWarehouse: null,
            currentVariantId: null,
            bomData: {},
            precision: 2,
            bomQuantity: null,
        });

        useSubEnv({
            overviewBus: new EventBus(),
        });

        onWillStart(async () => {
            var self = this;
            await self.render_dashboards();
            await self.render_graphsweekly();
            await self.render_graphsmonthly();
        });
        onMounted(() => {
            // do something
            var self = this;
            self.datadisplay();
                 self.render_graphsweekly();
            self.render_graphsmonthly();

        });
        onPatched(() => {
            // do something
            var self = this;
            self.render_dashboards();
            self.render_graphsweekly();
            self.render_graphsmonthly();
        });
    }
        async render_dashboards() {
     var self = this;
     var result = await this.orm.call("tour.reservation", "get_count_list", [])
        var TourDashboardView = renderToElement('TourDashboardView', {});
        return TourDashboardView

    }
    async datadisplay() {
        var result = await this.orm.call("tour.reservation", "get_count_list", [])
        $('.total-booking').text(result.total_booking)
        $('.last-week-date').text(result.last_week)
        $('.today-booking').text(result.today_booking)
        $('.last-month-date').text(result.last_month)
}

     today_booking() {
     var self = this;
        var timeElapsed = Date.now();
        var today = new Date(timeElapsed)
        today.toLocaleDateString();
        this.actionService.doAction({
           name: "Tour Booking",
            type: 'ir.actions.act_window',
            res_model: 'tour.reservation',
            view_mode: 'tree,form',
            view_type: 'list',
            views: [[false, 'list'],[false, 'form']],
            views: [[false, 'list'],[false, 'form']],
            context: {
                        'search_default_today_appointment':true,
                    },
            domain: [['booking_date','=',today]],
            target: 'current'
        });
    }


    last_week_booking() {
        this.actionService.doAction({
            name: "Tour Booking",
            type: 'ir.actions.act_window',
            res_model: 'tour.reservation',
            view_mode: 'tree,form',
            view_type: 'list',
            views: [[false, 'list'],[false, 'form']],
            views: [[false, 'list'],[false, 'form']],
            context: {
                        'search_default_tour_booking_last_week':true,
                    },
            domain: [],
            target: 'current'
        });
    }

    last_month_booking() {
        this.actionService.doAction({
            name: "Tour Booking",
            type: 'ir.actions.act_window',
            res_model: 'tour.reservation',
            view_mode: 'tree,form',
            view_type: 'list',
            views: [[false, 'list'],[false, 'form']],
            views: [[false, 'list'],[false, 'form']],
//            context: {
//                        'search_default_tour_booking_last_week':true,
//                    },
            domain: [],
            target: 'current'
        });
    }

        total_booking() {
        this.actionService.doAction({
            name: "Tour Booking",
            type: 'ir.actions.act_window',
            res_model: 'tour.reservation',
            view_mode: 'tree,form',
            view_type: 'list',
            views: [[false, 'list'],[false, 'form']],
            views: [[false, 'list'],[false, 'form']],
            context: {
                        'search_default_total':true,
                    },
            domain: [],
            target: 'current'
        });
    }




     async render_graphsmonthly() {
        var self = this;
        var ctx = $('#monthly_booking')
        Chart.plugins.register({
            beforeDraw: function(chartInstance) {
                var ctx = chartInstance.chart.ctx;
                ctx.fillStyle = "white";
                ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
            }
        });
        var bg_color_list = []
        for (var i = 0; i <= 12; i++) {
            bg_color_list.push(self.getRandomColor())
        }
        var result = await this.orm.call("tour.reservation", "get_monthly_booking", [])
        if (result) {
            var data = result.data
            var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                'August', 'September', 'October', 'November', 'December'
            ]
            var month_data = [];

            if (data) {
                for (var i = 0; i < months.length; i++) {
                    months[i] == data[months[i]]
                    var day_data = months[i];
                    var month_count = data[months[i]];
                    if (!month_count) {
                        month_count = 0;
                    }
                    month_data[i] = month_count

                }
            }
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {

                    labels: months,
                    datasets: [{
                        label: 'Monthly Tour',
                        data: month_data,
                        backgroundColor: bg_color_list,
                        borderColor: bg_color_list,
                        borderWidth: 1,
                        pointBorderColor: 'white',
                        pointBackgroundColor: 'red',
                        pointRadius: 1,
                        pointHoverRadius: 10,
                        pointHitRadius: 30,
                        pointBorderWidth: 1,
                        pointStyle: 'rectRounded'
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                min: 0,
                                max: Math.max.apply(null, month_data),
                            }
                        }]
                    },
                    responsive: true,
                    maintainAspectRatio: true,
                    leged: {
                        display: true,
                        labels: {
                            fontColor: 'black'
                        }
                    },
                },
            });

        };

    }
    getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }
    async render_graphsweekly() {
        var self = this;
        var ctx = $('#weekly_booking')
        Chart.plugins.register({
            beforeDraw: function(chartInstance) {
                var ctx = chartInstance.chart.ctx;
                ctx.fillStyle = "white";
                ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
            }
        });
        var bg_color_list = []
        for (var i = 0; i <= 12; i++) {
            bg_color_list.push(self.getRandomColor())
        }
        var result = await this.orm.call("tour.reservation", "get_weekly_booking", [])
        if (result) {
            var data = result.data
            var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                'August', 'September', 'October', 'November', 'December'
            ]
            var month_data = [];

            if (data) {
                for (var i = 0; i < months.length; i++) {
                    months[i] == data[months[i]]
                    var day_data = months[i];
                    var month_count = data[months[i]];
                    if (!month_count) {
                        month_count = 0;
                    }
                    month_data[i] = month_count

                }
            }
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {

                    labels: months,
                    datasets: [{
                        label: 'Weekly Tour',
                        data: month_data,
                        backgroundColor: bg_color_list,
                        borderColor: bg_color_list,
                        borderWidth: 1,
                        pointBorderColor: 'white',
                        pointBackgroundColor: 'red',
                        pointRadius: 1,
                        pointHoverRadius: 10,
                        pointHitRadius: 30,
                        pointBorderWidth: 1,
                        pointStyle: 'rectRounded'
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                min: 0,
                                max: Math.max.apply(null, month_data),
                            }
                        }]
                    },
                    responsive: true,
                    maintainAspectRatio: true,
                    leged: {
                        display: true,
                        labels: {
                            fontColor: 'black'
                        }
                    },
                },
            });

        };

    }



}

TourDashboard.template = "TourDashboardView";

registry.category("actions").add("Tour_dashboard", TourDashboard);
