import React from 'react';
import Textarea from './Textarea';

export default class GoalDetails extends React.Component {
  static propTypes = {
    next: React.PropTypes.func.isRequired,
  };

  state = {
    isValid: false,
  };

  next(event) {
    this.props.next({
      name: this._name.value,
      text: this._textarea.getValue(),
    });
    event.preventDefault();
  }

  render() {
    const placeholder = 'Tip: What you write is up to you but try to be specific, eg ' +
        'you might want to write for an amount of time or to a word ' +
        'count, or on a specific project.';

    return (
        <div className="page">
          <section>
            <p>Welcome to the challenge! It’s great to have you on
              board.</p>

            <p>Your first task is to set a writing goal.</p>

            <p><strong>What do you want to achieve with your writing in
              the next 5 days?</strong></p>
          </section>

          <div>
            Goal Name: <input
                ref={input => this._name = input}
                type="text" />
            <Textarea
                ref={input => this._textarea = input}
                onChange={isValid => this.setState({ isValid })}
                placeholder={placeholder} />
          </div>

          <section>
            <p>Still struggling? Check out our blog on <a
                href="http://blog.write-track.co.uk/how-to-set-a-writing-goal/">how
              to set a goal</a>.</p>

            <p>All done? Great! Next, you need to set a step to help
              you achieve your goal.</p>
          </section>

          <p>
            <button id="next" className="gutter" disabled={!this.state.isValid} onClick={this.next.bind(this)}>Next &raquo;</button>
          </p>
        </div>
    );
  }
}