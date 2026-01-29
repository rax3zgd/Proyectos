alert("Benvingut/da a la meva pagina web");

var nom = prompt("Com et dius?");
alert("Hola "+nom+" gracies per visitar-nos!");
console.log(nom);
/* */
let edat = prompt("Cual es tu edat");
let esmajor;

function mayorEdat(nom,edat){

    if (edat<12){
        return console.log(nom+": Ets un nen/a.")
    }else if(edat>=12 && edat<=17){
        return console.log(nom+": Ets un/a adolescent.")
    }else if(edat>=18 && edat<=64){
        return console.log(nom+": Ets un adult.")
    }else if(edat>=65){
        return console.log(nom+": Ets una persona gran.")
    }else{
        return console.log("Edad invalida")        
    }
}
let result = mayorEdat(nom,edat);

function mayorEdatSwitch(nom,edat){

    switch (true){
        case (edat<12):
            return console.log(nom+": Ets un nen/a.")

        case (edat>=12 && edat<=17):
            return console.log(nom+": Ets un/a adolescent.")

        case (edat>=18 && edat<=64):
            return console.log(nom+": Ets un adult.")
            
        case (edat>=65):
            return console.log(nom+": Ets una persona gran.")

        default:
            return console.log("Edad invalida")        
    }
}

result = mayorEdatSwitch(nom,edat);