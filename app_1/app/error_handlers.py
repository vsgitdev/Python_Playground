from app import app



from flask import render_template, request


@app.errorhandler(404)
def not_found(e):
    return render_template("public/error_templates/404.html")

@app.errorhandler(500)
def server_error(e):

    app.logger.error(f'Server error: {e}, route: {request.url}')

    # email_admin(message="Server error", error=e, url=request.url )
    
    return render_template("public/error_templates/500.html")

@app.errorhandler(403)
def forbidden(e):

    app.logger.error(f'Forbidden access: {e}, route: {request.url}')

   
    return render_template("public/error_templates/403.html")



# @app.errorhandler(403)
# def not_found(e):
#     return render_template("public/error_templates/403.html")