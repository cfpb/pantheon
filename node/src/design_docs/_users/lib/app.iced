module.exports = 
  views:
    by_resource_id:
      map: (doc) ->
        for resource_name, resource of doc.rsrcs
          resource_id = resource.id
          if resource_id
            emit([resource_name, resource_id], doc.name)
    by_resource_username:
      map: (doc) ->
        for resource_name, resource of doc.rsrcs
          resource_username = resource.username || resource.login
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
    by_auth:
      map: (doc) ->
        for role in doc.roles
          out = role.split('/')
          out.push(doc.name)
          emit(out)
    contractors:
      map: (doc) ->
        emit(doc.data?.contractor or false, doc.username)
  lists:
    get_users: (header, req) ->
      out = []
      while(row = getRow())
        doc = row.doc
        delete doc.password_scheme
        delete doc.iterations
        delete doc.derived_key
        delete doc.salt
        out.push(doc)
      return JSON.stringify(out)
    get_doc: (header, req) ->
      row = getRow()
      if row
        return JSON.stringify(row.doc)
      else
        throw(['error', 'not_found', 'document matching query does not exist'])
  rewrites: [
    {
      from: "/users",
      to: "/_list/get_users/by_username",
      method: 'GET',
      query: {include_docs: 'true'},
    },
    {
      from: "/users/:user_id",
      to: "../../:user_id",
      query: {},
    },
  ]
  validate_doc_update: (newDoc, oldDoc, userCtx, secObj) ->

