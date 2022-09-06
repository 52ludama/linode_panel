/**
 * For usage, visit Chart.js docs https://www.chartjs.org/docs/latest/
 */
// const pieConfig = {
//   type: 'doughnut',
//   data: {
//     datasets: [
//       {
//         data: [33, 33, 33],
//         /**
//          * These colors come from Tailwind CSS palette
//          * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
//          */
//         backgroundColor: ['#0694a2', '#1c64f2', '#7e3af2'],
//         label: 'Dataset 1',
//       },
//     ],
//     labels: ['Shoes', 'Shirts', 'Bags'],
//   },
//   options: {
//     responsive: true,
//     cutoutPercentage: 80,
//     /**
//      * Default legends are ugly and impossible to style.
//      * See examples in charts.html to add your own legends
//      *  */
//     legend: {
//       display: false,
//     },
//   },
// }
//
// // change this to the id of your chart element in HMTL
// const pieCtx = document.getElementById('pie')
// window.myPie = new Chart(pieCtx, pieConfig)

const pieConfig_1 = {
          chaoguo: get_transfer_info()['billable'].toFixed(2),
          used:(get_transfer_info()['used']/1000000000).toFixed(2),
          shengyu: (get_transfer_info()['quota']-this.used).toFixed(2),
          sum: this.chaoguo + this.used + this.shengyu,
          m1: Number((this.chaoguo/this.sum*100).toFixed(0)),
          m2: Number((this.used/this.sum*100).toFixed(0)),
          m3: Number((this.shengyu/this.sum*100).toFixed(0)),
          type: 'doughnut',
          data: {
            datasets: [
              {
                // data: [this.m1,this.m3,this.m2],
                data: [10,20,30],
                /**
                 * These colors come from Tailwind CSS palette
                 * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
                 */
                backgroundColor: ['#0694a2', '#1c64f2', '#7e3af2'],
                label: 'transfer_info',
              },
            ],
            labels: ['超额', '剩余', '使用'],
          },
          options: {
            responsive: true,
            cutoutPercentage: 80,
            /**
             * Default legends are ugly and impossible to style.
             * See examples in charts.html to add your own legends
             *  */
            legend: {
              display: false,
            },
          },
        }

        // change this to the id of your chart element in HMTL
        const pieCtx_1 = document.getElementById('pie_1')
        window.myPie = new Chart(pieCtx_1, pieConfig_1)

function get_transfer_info(){
          var transfer_info_list;
          $.ajax({
                            type: "GET",
                            url: "https://api.linode.com/v4/linode/instances/{{ linode_server.linode_id }}/transfer",
                            async:false,
                            headers: {"Authorization": "Bearer {{ token_key }}"},
                            contentType: "application/json;charset=UTF-8",
                            dataType: "json",
                            success:function(result){
                                transfer_info_list = result
                            },
                        });
        return transfer_info_list
        }
