window.onload = function() {
  var body = document.getElementsByTagName("body")[0];
  var inputRows = document.getElementById("input-rows");
  var inputColumns = document.getElementById("input-columns");
  var inputMatrix = document.getElementById("input-matrix");
  var inputMessage = document.getElementById("input-message");
  var form = document.getElementsByTagName("form")[0];
  var inputEncrypt = document.getElementById("encrypt");
  var inputDecrypt = document.getElementById("decrypt");
  var labels = document.getElementsByClassName("fancy-label");
  var inputs = document.getElementsByClassName("fancy-input");
  console.log({ labels, inputs });

  function handleUserNameInputChange(e) {
    console.log(e);
    if (e.target.value == "") {
      console.log("empty");
    }
  }

  function handleFancyInputClickAndKey(label, input) {
    return function(e) {
      console.log(e);
      label.style.display = "initial";
      input.placeholder = "";
    };
  }

  function handleBodyClick(e) {
    console.log(e);
    if (e.target != userInput && userInput.value == "") {
      label.style.display = "none";
      userInput.placeholder = "Twitch Username";
    }
  }

  for (var x = 0; x < labels.length; x++) {
    //inputs[x].onchange = handleUserNameInputChange(labels[x]);
    inputs[x].onclick = handleFancyInputClickAndKey(labels[x], inputs[x]);
    inputs[x].onkeypress = handleFancyInputClickAndKey(labels[x], inputs[x]);
  }

  function getOperation() {
    if (inputEncrypt.checked) return "encrypt";
    else if (inputDecrypt.checked) return "decrypt";
    else return "encrypt";
  }

  function convertToArray(str) {
    var matrix = [];

    str = str.trim();

    var regex = / /gi;

    str = str.replace(regex, " ");

    var rows = str.split("\n");

    rows.forEach(function(row) {
      console.log(row);
      matrix.push(
        row.split(" ").map(function(el) {
          return Number(el);
        })
      );
    });

    return transposeArray(matrix, matrix.length).flat();
  }

  function transposeArray(array, arrayLength) {
    var newArray = [];
    for (var i = 0; i < array.length; i++) {
      newArray.push([]);
    }

    for (var i = 0; i < array.length; i++) {
      for (var j = 0; j < arrayLength; j++) {
        newArray[j].push(array[i][j]);
      }
    }

    return newArray;
  }

  form.onsubmit = async function(e) {
    e.preventDefault();
    var requestBody = {
      hasher: {
        rows: Number(inputRows.value),
        columns: Number(inputColumns.value),
        data: convertToArray(inputMatrix.value)
      },
      message: inputMessage.value,
      operation: getOperation()
    };
    console.log(requestBody);

    const url =
      "https://10qk6aepkb.execute-api.us-west-2.amazonaws.com/staging/matrix-fun/";

    const instance = axios.create({
      timeout: 1000,
      headers: {
        "Content-Type": "application/json",
        "x-api-key": "HvHEVC3pJB1gu5bwB44gw46nf5BGIAcR49m9KoLM"
      }
    });

    instance({
      method: "post",
      url,
      data: requestBody
    }).then(function(response) {
      console.log(response);
    });

    /*var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        alert(this.responseText);
      }
    };
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader(
      "x-api-key",
      "HvHEVC3pJB1gu5bwB44gw46nf5BGIAcR49m9KoLM"
    );
    xhttp.send(JSON.stringify(requestBody));*/

    /*try {
      const response = await fetch(url, {
        method: "POST",
        mode: "no-cors",        
        headers: {
          "Content-Type": "application/json",
          "x-api-key": "HvHEVC3pJB1gu5bwB44gw46nf5BGIAcR49m9KoLM"
        },
        body: JSON.stringify({
          hasher: {
            data: [1, 2, 3, 4, 5, 7, 13, 15, 23],
            rows: 3,
            columns: 3
          },
          message: "Hello. My name is Jeff.",
          operation: "encrypt"
        })
      });
      const json = await response.text();
      console.log("Success:", JSON.stringify(json));
    } catch (error) {
      console.error("Error:", error);
    }*/
  };

  //body.onclick = handleBodyClick;
};
