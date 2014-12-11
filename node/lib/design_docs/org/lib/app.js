exports.views = {
  by_type: {
    map: function(doc) {
      var team_data;
      team_data = require('views/lib/team_data').parse(doc._id);
      if (!team_data) {
        return;
      }
      return emit([team_data.team, team_data.typ, team_data.name], 1);
    }
  }
};