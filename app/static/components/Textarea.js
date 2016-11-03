import React from 'react';

export default class Textarea extends React.Component {
    static propTypes = {
        onChange: React.PropTypes.func.isRequired,
        required: React.PropTypes.bool,
        wordLimit: React.PropTypes.number,
        placeholder: React.PropTypes.string,
    };

    static defaultProps = {
        required: true,
        wordLimit: 100,
    };


    state = {
        wordsLeft: 100,
        isValid: false,
    };

    componentWillMount() {
        this.setState({wordsLeft: this.props.wordLimit});
    }

    onChange(event) {
        const value = event.target.value;
        const { wordLimit } = this.props;

        const wordsLeft = wordLimit - this.getWords(value).length;

        this.setState({ wordsLeft });

        this.props.onChange(value, this.isValid(value));
    }

    getWords(value) {
        value = value || this.props.value;

        return value.split(' ').filter(function (word) {
            return word.length > 0;
        });
    }

    isValid(value) {
        const words = this.getWords(value);
        const { wordLimit, required } = this.props;

        if (required) {
            return words.length > 0 && words.length <= wordLimit;
        } else {
            return words.length <= wordLimit;
        }
    }

    render() {
        return (
            <div>
                <textarea
                    rows={8}
                    placeholder={this.props.placeholder}
                    className="manualLimit"
                    onChange={this.onChange.bind(this)}
                    value={this.props.value}
                />
                <p>{this.state.wordsLeft} words remaining</p>
            </div>
        );
    }
}
