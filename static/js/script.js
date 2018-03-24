
    function InvoiceShow(){
      $('#id_invoice_content').css('display','block');
      $('#dispath_table').css('display','none');
    }
       function DispathShow(){
      $('#id_invoice_content').css('display','none');
      $('#dispath_table').css('display','block');
    }



    $('#invoice_add_id').click(function(){

    });
    $("#id_send").click(function(){
        $.ajax({
          type:"POST",
          url:"",
          data:{
            'model':id_model_cart.value,
            'amount':id_amount.value,
            'post_office':id_post_offices.value,
            'date_disp':id_date_send.value,

            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()
          },
          //success: function(html){$("#id_body").html(html);},
          success:Success,
          //error: alert('---'),
          error:function(html){$("#id_body").html(html);alert(html.responseText);},
          dataType:'html'
        });
        //id_resp_stat.innerHTML='';
        //id_resp_stat.style.display='none';

    });
    function func() {
  id_resp_stat.style.transition='5s';
  id_resp_stat.style.opacity=0;
}
    function func1() {
  id_resp_stat.style.display='none';
}


    function ErrorSend(){
    		id_resp_stat.style.display='block';
    		id_resp_stat.innerHTML='<strong>Ошибка!</strong>';
    		id_resp_stat.style.margin='5px';
    		id_resp_stat.className ='alert alert-danger';

    		//id_resp_stat.style.transition='1s';
    		id_resp_stat.style.transition='top 2s ease-out 2s';
    		id_resp_stat.style.opacity=1;
    		setTimeout(func, 3000);
    		setTimeout(func1, 7000);


    }
function SuccessHide(){
  $('#success_dispath_id').hide();
}
        function Success(data, textStatus, jqXHR)
{
  var con=jqXHR.responseText;
  var response=jqXHR.responseText;
  //var position_begin=con.indexOf('<table class="table" style="width: 100%;" id="dispath_table">');
  var position_begin=con.indexOf('<table class="table" style="width: 100%;" id="dispath_table">');
  var position_end=con.indexOf('</table><span style="display:none">end_table</span>');
  //var position_end=con.indexOf('<span style="color:none;font-size:1px;">end_table</span></div>');
  //alert(con);
  id_table_content.innerHTML=con.substring(position_begin, position_end);
  //var balance_for_month=
  //var disp_for_month=
  //var balance=
  panel_body_balance.innerHTML=response.substring(response.indexOf('<div class="panel-body" id="panel_body_balance">'),response.indexOf('</div><div id="panel_body_balance_end_tag" hidden=""></div>'));
  //$('#panel_body_balance').html(response.substring(response.indexOf('<div class="panel-body" id="panel_body_balance">'),response.indexOf('</div><div id="panel_body_balance_end_tag" hidden=""></div>')));
  $('#message_success_id').text('<strong style="font-size:18px;">Отправка записанна!</strong>');
  $('#success_dispath_id').show();
  setTimeout(SuccessHide, 7000);
  /*id_resp_stat.style.display='block';
  id_resp_stat.innerHTML='<strong><p>Успешная операция!</p></strong>';
  id_resp_stat.style.margin='5px';
  id_resp_stat.className ='alert alert-success';

  id_resp_stat.style.transition='1s';
  id_resp_stat.style.opacity=1;
  setTimeout(func, 3000);
  setTimeout(func1, 7000);*/

}

        $("#id_run_report").click(function(){
        	var date_for_report=current_period.value;
        	n=String(date_for_report).replace('.','');
        	d=n.split('');
        	month=d[0]+d[1];
        	year=d[2]+d[3]+d[4]+d[5];
        $.ajax({
          type:"POST",
          url:"",
          data:{
            'month':month,
            'year':year,
            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()
          },
          success: DownloadReport,
          //error:alert('ERROR'),
          dataType:'html'
        });

    });
        function DownloadReport(){
        	//document.location.href="{{report_file}}";
        	document.location.replace("{{report_file}}");
        }

  function Filter_for_date(){
        $.ajax({
          type:"POST",
          url:"",
          data:{
            'f_in':id_f_in.value,
            'f_out':id_f_out.value,
            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()
          },
          success:searchSuccess,
          //success:function(data){
          //  $('#id_table_content').text(data.id_table_content);
          //},

          //error: alert('---'),
          dataType:'html'
        });

    }



    function searchSuccess(data, textStatus, jqXHR)
{
  var con=jqXHR.responseText;
  var response=jqXHR.responseText;
  var position_begin=con.indexOf('<table class="table" style="width: 100%;" id="dispath_table">');
  var position_end=con.indexOf('</table><span style="display:none">end_table</span>');
  //var position_end=con.indexOf('<span style="color:none;font-size:1px;">end_table</span></div>');
  //alert(con);
  id_table_content.innerHTML=con.substring(position_begin, position_end);
  //var balance_for_month=
  //var disp_for_month=
  //var balance=
  panel_body_balance.innerHTML=response.substring(response.indexOf('<div class="panel-body" id="panel_body_balance">'),response.indexOf('</div><div id="panel_body_balance_end_tag" hidden=""></div>'));
  //$('#panel_body_balance').html(response.substring(response.indexOf('<div class="panel-body" id="panel_body_balance">'),response.indexOf('</div><div id="panel_body_balance_end_tag" hidden=""></div>')));
}
  function RefreshAfterDispDelete(data, textStatus, jqXHR){
    var con=jqXHR.responseText;
    var response=jqXHR.responseText;
  var position_begin=con.indexOf('<table class="table" style="width: 100%;" id="dispath_table">');
  var position_end=con.indexOf('</table><span style="display:none">end_table</span>');
  //var position_end=con.indexOf('<span style="color:none;font-size:1px;">end_table</span></div>');
  //alert(con);
  id_table_content.innerHTML=con.substring(position_begin, position_end);
    panel_body_balance.innerHTML=response.substring(response.indexOf('<div class="panel-body" id="panel_body_balance">'),response.indexOf('</div><div id="panel_body_balance_end_tag" hidden=""></div>'));
    alert('Отправка удалена');
}


function DeleteDispath(id){
          $.ajax({
          type:"POST",
          url:"",
          data:{
            'delete_id':id,
            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()
          },
          success:RefreshAfterDispDelete,
          dataType:'html'
        });
}

$('#btn_add_invoice_id').click(function(){
            $.ajax({
              type:"POST",
              url:"",
              data:{
                'model_c_invoice':$('#invoice_model_c_id').val(),
                'count_invoice':$('#invoice_count_id').val(),
                'invoice_invoice':$('#invoice_doc_id').val(),
                'type_c_invoice':$('#invoice_type_id').val(),
                'status_invoice':$('#invoice_status_id').val(),
                'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()
              },
              //success: function(html){$("#id_body").html(html);},
              success:SuccessAddInvoice,
              //error: alert('---'),
              error:function(html){$("#id_body").html(html);alert(html.responseText);},
              dataType:'html'
            });
              });
          function DeleteInvoice(id){
          $.ajax({
          type:"POST",
          url:"",
          data:{
            'delete_invoice_id':id,
            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()
          },
          success:RefreshAfterInvoiceDelete,
          dataType:'html'
        });
      }
        function RefreshAfterInvoiceDelete(data, textStatus, jqXHR){
          var con=jqXHR.responseText;
          $('#id_invoice_content').css('display','block');

        var position_begin=con.indexOf('<table class="table" style="width: 100%;" id="invoice_table">');
        var position_end=con.indexOf('<span style="display:none">end_table2</span>');
          id_invoice_content.innerHTML=con.substring(position_begin, position_end);

          alert('Накладная удалена');


      }
       function SuccessAddInvoice(data, textStatus, jqXHR){
        var con=jqXHR.responseText;
        $('#id_invoice_content').css('display','block');

        var position_begin=con.indexOf('<table class="table" style="width: 100%;" id="invoice_table">');
        var position_end=con.indexOf('<span style="display:none">end_table2</span>');
        id_invoice_content.innerHTML=con.substring(position_begin, position_end);

          /*var position_begin=con.indexOf('<table class="table" style="width: 100%;" id="dispath_table">');
          var position_end=con.indexOf('</table><span style="display:none">end_table</span>');
          id_table_content.innerHTML=con.substring(position_begin, position_end);*/

        $('#success_dispath_id').show();
          setTimeout(SuccessHide, 7000);
      }
