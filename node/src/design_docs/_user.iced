module.exports =
  base:
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
      contractors:
        map: (doc) ->
          emit(doc.data?.contractor or false, doc.username)