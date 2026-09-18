
function Enviar() {

    var listFields = document.getElementById('listFields');
    var listKeys = document.getElementById('listKeys');
    var selColumns = document.getElementById('selColumns');
    var selKeyFields = document.getElementById('selKeyFields')

    const formMain = document.forms['formMain'];
    var list= '';

    for (let index = 0; index < selColumns.length; index++) {
        if (list == '') 
            list = selColumns.options[index].text;
        else
            list = list + '\n' + selColumns.options[index].text;
    }

    listFields.value = list;
    list = '';

    for (let index = 0; index < selKeyFields.length; index++) {
        if (list == '') 
            list = selKeyFields.options[index].text;
        else
            list = list + '\n' + selKeyFields.options[index].text;
    }

    listKeys.value = list;

    formMain.submit();
}

function ClearList(list) {

    for (let index = list.options.length - 1; index >= 0; index--) {
        list.remove(index);
    }
}

function AddKeyList() {

    var selKeyFields = document.getElementById('selKeyFields');
    var selColumns = document.getElementById('selColumns');

    var exist = false;

    for (let index = 0; index < selColumns.length; index ++) {
        if (selColumns.options[index].selected == true ) {            
            exist = false; 
            for (let index2 = 0; index2 < selKeyFields.length; index2++) {
                if (selKeyFields.options[index2].value == selColumns.options[index].value) {
                    exist = true;
                    break;
                }
            }

            if (!exist) {
                field = selColumns.options[index].text.split(' ');             
                const newOption = new Option( selColumns.options[index].value, field[0]);
                selKeyFields.appendChild(newOption);
            }
        }
    }  
}

function FieldSelect(_object) {

    var listField = document.getElementById('selColumns');
    var index = listField.selectedIndex;
    var field = undefined;
    var TypeField = document.getElementById('selType');
    var SizeField = document.getElementById('txtSize');

    if (listField.options[index].selected == true ) {
        field = listField.options[index].text.split(' '); 
        TypeField.value = field[1];

        if (field[2] == undefined)
            SizeField.value = '';
        else
            SizeField.value = field[2];
    }

}

function SelectType_Input (_object) {

    var defaultType = _object.value;
    console.log(defaultType)
    var listField = document.getElementById("selColumns");
    var field = undefined;

    for (let index = 0; index < listField.length; index ++) {
        if (listField.options[index].selected == true ) {
            field = listField.options[index].text.split(' '); 
            listField.options[index].text = field[0] + ' ' + defaultType + ' ' + (field[2] == undefined? '':field[2]);
        }
    }  
}

function Size_Input (_object) {

    var value = _object.value;
    var listField = document.getElementById("selColumns");
    var field = undefined;

    if (value == undefined)
        value = '';

    for (let index = 0; index < listField.length; index ++) {
        if (listField.options[index].selected == true ) {
            field = listField.options[index].text.split(' '); 
            listField.options[index].text = field[0] + ' ' + field[1] + ' ' + value;
        }
    }  

}

function DataText_Input (_object) {

    var radios = document.querySelectorAll('input[name="rdDelimiter"][type="radio"]');
    var defaultType = document.getElementById("selType").value;
    var defaultsize = document.getElementById("txtSize").value;
    var delimiter_type = undefined;
    var delimiter;
    var text = _object.value.split('\n')[0];

    // Itera sobre a lista de botões radio para encontrar o selecionado
    for (let i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            delimiter_type = radios[i].value;
            break; // Encontrou o elemento, não precisa continuar a iteração
        }
    }

    switch ( delimiter_type ) {
        case 'other':
            delimiter = document.getElementById("txtOther").value;
            break;
        case 'tab':
            delimiter = '\t';
            break;
        case 'semicolon':
            delimiter = ';';
            break;
        case 'fixed':
            //delimiter = 'TODO: fixed';
            alert('Not implemented!');
            return;
    }

    const columns = text.split(delimiter);
    listField = document.getElementById("selColumns");

    ClearList(listField);
    
    for (let index = 0; index < columns.length; index++) {
        const newOption = new Option(columns[index] + ' ' + defaultType + ' ' + defaultsize, columns[index]);
        listField.appendChild(newOption);
    }

    
}

function Copy(text) {

  try {
    navigator.clipboard.writeText(text);
    console.log('copiado para a área de transferência!');
  } catch (err) {
    console.error('Falha ao copiar texto: ', err);
  }
}
