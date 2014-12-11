module.exports = 
  views:
    by_resource_id:
      map: (doc) ->
        for resource_name of doc.resrcs
          resource = doc.resrcs[resource_name]
          resource_id = resource.data.id
          emit([resource_name, resource_id], doc.name)
    by_resource_username:
      map: (doc) ->
        for resource_name of doc.resrcs
          resource = doc.resrcs[resource_name]
          resource_username = resource.data.username || resource.data.login
          if resource_username
            emit([resource_name, resource_username], doc.name)
    by_username:
      map: (doc) ->
        if doc.username
          emit(doc.username)
    by_name:
      map: (doc) ->
        if doc.name
          emit(doc.name)
    contractors:
      map: (doc) ->
        emit(doc.data?.contractor or false, doc.username)
  lists:
    all_users: (header, req) ->
      out = []
      while(row = getRow())
        out.push(row.doc)
      return JSON.stringify(out)
  rewrites: [
    {
      from: "/users",
      to: "/_list/all_users/by_username",
      method: 'GET',
      query: {include_docs: 'true'},
    },
    {
      from: "/users/:user_id",
      to: "../../:user_id",
      query: {},
    },
  ]
