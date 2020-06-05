// Variables
var justePrix = 0
var imageUrl = ""
var prixSaisie = 0
var nbEssai = 0
var nbEssaiMax = 0
var gagne = false

$("#jeu").hide()
$("#gagne").hide()
$("#perdu").hide()

// requete commencer une partie
$("#start_partie").click(function(){
    $("#jeu").hide()
    $("#perdu").hide()
    justePrix = 0
    description = ""
    imageUrl = ""
    prixSaisie = 0
    $("#prixSaisie").val(0)
    nbEssai = 0
    $("#nb_essai").text(0)
    $("#resultat").text("")
    $("#div_img_article").empty()
    gagne = false

    // init gagne
    $("#img_gagne")
        .animate({            
            width : '-=500px',
            height : '-=500px'
        })  
    $("#gagne").hide()  
    // init perdu
    $("#img_perdu")
        .animate({            
            width : '-=300px',
            height : '-=300px'
        })  
    $("#perdu").hide()  

    // niveau de difficulté
    switch ($("#niveau").val()){
        case "Facile : 50 essais":
            nbEssaiMax = 50
            break
        case "Moyen : 25 essais":
            nbEssaiMax = 25
            break
        case "Difficile : 10 essais":
            nbEssaiMax = 10
            break            
    }

    $.ajax({
        url: "/initJustePrix?nbEssaiMax="+ nbEssaiMax,
        success: initJustePrix,
        error: function (xhr, ajaxOptions, thrownError) {
          //console.log(thrownError); 
          }
      });
    
    function initJustePrix(result){
        justePrix = result["justePrix"]
        console.log("Juste Prix : " + result["justePrix"])
        //console.log("juste prix : " + result["justePrix"])
        $("#jeu").show()

        // Affichage de l'article
        $("#description").text(result["description"])
        $("#div_img_article").append('<img id="img_article" src="' + result["imageUrl"] + '"></img>')

        gagne = false
    }  
});


// requete de test prix
$("#prixSaisie").change(function () 
    {
    prixSaisie = $("#prixSaisie").val()

    // nb d'essai
    nbEssai = nbEssai + 1
    $("#nb_essai").text(nbEssai)

    $.ajax({
        url: "/testPrixSaisie?prixSaisie="+ prixSaisie,
        success: testPrix,
        error: function (xhr, ajaxOptions, thrownError) {
        //console.log(thrownError); 
        }
    });

    function testPrix(result){
        // affichage du temps de la partie
        //console.log("temps de la partie : " + result["tpsPartie"])
        $("#tps_partie").text(result["tpsPartie"])
        
        // Resultat
        switch(result["resultat"]){
            case "jp+":
                $("#resultat").text("C'est plus chère !")
                break

            case "jp-":
                $("#resultat").text("C'est moins chère !")
                break 

            case "jp":
                $("#resultat").text("")
                $("#jeu").hide()
                $("#gagne").show()
                // animation image
                $("#img_gagne")
                .animate({            
                    width : '+=700px',
                    height : '+=700px'
                })                
                .animate({
                    width: '-=200px',
                    height: '-=200px'
                })
                gagne = true
                break

            default:
                break
        }

        // Perdu !
        if (nbEssai >= nbEssaiMax && gagne == false){
            $("#resultat").text(nbEssaiMax + " essai maximum ... Perdu !")
            $("#perdu").show()
                // animation image
                $("#img_perdu")
                .animate({            
                    width : '+=200px',
                    height : '+=200px'
                })                
                .animate({
                    width: '-=100px',
                    height: '-=100px'
                })
            $("#jeu").hide()    
        }
    }  
});

