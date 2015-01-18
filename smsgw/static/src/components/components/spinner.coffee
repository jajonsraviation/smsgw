###
See for more information
http://arcturo.github.io/library/coffeescript/07_the_bad_parts.html
@cjsx React.DOM
###
"use strict"

React = require 'react'

module.exports = React.createClass
    render: ->
        classNames = ['spinner']
        classNames.push 'fullscreen' if this.props.fullscreen

        <div className={classNames.join ' '}>
            <div className="dots">
                Loading...
            </div>
        </div>