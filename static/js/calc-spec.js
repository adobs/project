


describe("My Test Suite", function(){

    it("should return HTML", function(){
        var html = getHtml("True", 1, "Mountain View, CA", "MarcSc89", "MarcSc89", 1, "hook-up");
        expect(html).toBe('<div id="content"><h1>There are <b>1</b> profiles in'+
                            ' Mountain View, CA</h1><h2>matching your search'+
                            '</h2><button type="button" class="btn btn-primary'+
                            ' btn-sm" data-toggle="modal" data-target="#myModal"'+
                            ' data-recipients="MarcSc89">Message Profiles in '+
                            'Montain View, CA</button><h1>The most commonly '+
                            'used adjective is <b>hook-up</b></h1><h2>(1 '+
                                'occurences)</h2><button type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#myModal"data-recipients="ExoticandErotic1">Message Profiles with hook-up</button></div>');

    });




});

