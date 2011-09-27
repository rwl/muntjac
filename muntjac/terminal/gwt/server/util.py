
def contextPath(request):
    ## FIXME: implement request.contextPath()
    return request.serverSideContextPath()


def originalContextPath(request):
    ## FIXME: implement request.originalContextPath()
    return contextPath(request)
