/*Функция дорисовывания нуля для методов getDate() и getMonth()*/
function BolsheDesyati(val){
  if( val < 10 ){
    return String(0)+String(val)
  }else{
    return String(val)
  }
}
/*Функция отрисовывания таблицы на основе JSON объекта*/
function RenderDispTable(dispatch){
  dispatch=JSON.parse(dispatch);
  l=[`<tr>
          <td><span><b>№</b></span></td>
          <td><span><b>Дата</b></span></td>
          <td><span><b>Модель</b></span></td>
          <td><span><b>Кол.</b></span></td>
          <td><span><b>Отделение</b></span></td>
 
          <td><span><b>Удалить</b></span></td>
      </tr>`];
for (i = 0; i < dispatch.length; i++) {
  //console.log(dispatch);
  let id=dispatch[i].id;
  date=new Date(dispatch[i].disp_date);
  let disp_date=BolsheDesyati(date.getDate())+'.'+BolsheDesyati(date.getMonth()+1)+'.'+date.getFullYear();
  let model=dispatch[i].model;
  let amount=dispatch[i].amount;
  let post_office=dispatch[i].post_office.toUpperCase();
  let post_index=dispatch[i].post_index;

  let s=`<tr><td style="width:15%;">${id}</td>
                <td><span><b>${disp_date}</b></span></td>
                <td><span>${model}</span></td>
                <td><span>${amount} шт.</span></td>
                <td><span>${post_office} / ${post_index}</span></td>
               
                <td><span id="delete_dispath_id" class="close text-center" onclick="DeleteDispath('${id}')" title="Удалить">X</span></td>
              </tr>`;
              l.push(s);
  }
  dispath_table.innerHTML=l.join(" ");
}
/*Полсе того как написали функцию сразу ее запускаем что бы отрисовалась таблица с отправками*/
$('body').ready(function(){
  $.ajax({
    type:"GET",
    url:"/api/dispatchs/?format=json",
      success:function(data, textStatus, jqXHR){RenderDispTable(jqXHR.responseText);},
      error:function(html){$("#id_body").html(html);alert(html.responseText);},
        dataType:'html'
  });
});
////////RenderDispTable(dispatch);
/*Создание отправки и отправка данных на сервер при помощи технологии AJAX, 
если все успешно то передаем ответ в функцию RenderDispTable(), 
которая отрисует актуальную таблицу по полученым данным, а если произошла ошибка то через функцию alert()
выведется ответ с сервера в котором будет содержание ошибки*/
$("#id_send").click(function(){
    $.ajax({
        type:"GET",
        url:"/create_dispatch",
        data:$('#create_disp_form_id').serializeArray(),
          success:function(data, textStatus, jqXHR){
            RenderDispTable(jqXHR.responseText);
            Success();},
          error:function(html){$("#id_body").html(html);alert(html.responseText);},
        dataType:'html'
        });
    });
/*функции анимации успешной отправки*/
function SuccessHide(){
  $('#success_dispath_id').animate({'opacity':'hide'});
}
function Success(){
  $('#message_success_id').text('<strong style="font-size:18px;">Отправка записанна!</strong>');
  $('#success_dispath_id').show();
  setTimeout(SuccessHide, 3000);
}
/*************************************/
/*функция удаления отправки*/
function DeleteDispath(id){
          $.ajax({
          type:"GET",
          url:"/delete_dispatch",
          data:{'delete_id':id,},
          success:function(data, textStatus, jqXHR){RenderDispTable(jqXHR.responseText);alert('Отправка удалена');},
          dataType:'html'
        });
}
/*Все что находится выше это рабочий код правка от 25.03.2018*/
/*****************************************************/
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
