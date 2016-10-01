import React from 'react';

export default class Textarea extends React.Component {
    static propTypes = {
        wordLimit: React.PropTypes.number,
        onChange: React.PropTypes.func,
        placeholder: React.PropTypes.string,
    };

    static defaultProps = {
        wordLimit: 100,
    };


    state = {
        wordsLeft: 100,
        isValid: false,
    };

    componentWillMount() {
        this.setState({ wordsLeft: this.props.wordLimit });
    }

    getValue() {
        return this.state.value;
    }

    onChange(event) {
        const value = event.target.value;
        console.log('Textarea.onChange "%s"', value);
        this.setState({value});

        const { wordLimit } = this.props;
        const words = value.split(' ').filter(function (word) {
            return word.length > 0;
        });

        const wordsLeft = wordLimit - words.length;
        this.setState({ wordsLeft });

        const nextValid = words.length > 0 && words.length <= wordLimit;
        const isValid = this.state.isValid;

        if (nextValid !== isValid) {
            this.setState({ isValid: nextValid });

            if (this.props.onChange) {
                this.props.onChange(nextValid);
            }
        }
    }

    render() {
        return (
            <div>
                <textarea
                    cols={40}
                    rows={10}
                    placeholder={this.props.placeholder}
                    className="manualLimit"
                    onChange={this.onChange.bind(this)}
                />
                <p>{this.state.wordsLeft} words remaining</p>
            </div>
        );
    }
}