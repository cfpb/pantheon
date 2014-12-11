module.exports =
  lib: require('./_lib')
  views:
    by_type:
      map: (doc) ->
        log('by_type', require('lib'), require('lib/get_team_data'))
        team_data = require('lib/get_team_data')(doc._id)
        if not team_data
          return
        emit([team_data.team, team_data.typ, team_data.name], 1)
  lists:
    teams:
      map: (head, req) ->
        out = {}
        while row = getRow()
          id_parts = doc._id.split('_')
          if id_parts[0] != 't'
            continue

    team:
      map: (head, req) ->
 
#       function(head, req) {
#     provides("html", function() {
#         html = "<html><body><ol>\n";
#         while (row = getRow()) {
#             html += "<li>" + row.key + ":" + row.value + "</li>\n";
#         }   
#         html += "</ol></body></head>";
#         return html;
#     }); 
# }