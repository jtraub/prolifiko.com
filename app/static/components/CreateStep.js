import React from 'react'
import Textarea from './Textarea';

export default class CreateStep extends React.Component {
  static propTypes = {
    prev: React.PropTypes.func.isRequired,
    submit: React.PropTypes.func.isRequired,
  };

  state = {
    isValid: false,
  };

  prev(event) {
    this.props.prev({ firstStep: this._textarea.getValue() });
    event.preventDefault();
  }

  submit(event) {
    this.props.submit({ firstStep: this._textarea.getValue() });
    event.preventDefault();
  }

  render() {
    const placeholder = 'Tip: Don’t think about the project as a whole. Just think ' +
        'about the one thing you can do next to progress your writing.';
    return (
        <div>
          <p>What’s the first step you can take to achieve your 5-day writing goal?</p>

          <div>
                    <Textarea
                        ref={input => this._textarea = input}
                        onChange={isValid => this.setState({ isValid })}
                        placeholder={placeholder}
                    ></Textarea>
          </div>

          <section>
            <p>Still struggling? Check out our blog on <a href="http://blog.write-track.co.uk/how-to-set-your-first-step/">how to set a first step</a>.</p>

            <p>
              <button id="previous" className="gutter" onClick={this.prev.bind(this)}>&laquo; Previous</button>
              <button id="submit" className="gutter" disabled={!this.state.isValid} onClick={this.submit.bind(this)}>Start! &raquo;</button>
            </p>
          </section>
        </div>
    );
  }
}