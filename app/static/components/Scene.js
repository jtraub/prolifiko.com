import React from 'react';
import _each from 'lodash.foreach';
import _merge from 'lodash.merge';
import decamelize from 'decamelize';

export default class Scene extends React.Component {

    static propTypes = {
        csrfToken: React.PropTypes.string.isRequired,
    };

    constructor(props) {
        super(props);

        this.state = {
            pageIndex: 0,
            pages: props.pages.map(page => ({
                name: page.name,
                component: page,
            })),
            data: props.pages.map(page => ({
                data: {},
                isValid: false,
            })),
        };

        this.next = this.next.bind(this);
        this.prev = this.prev.bind(this);
        this.submit = this.submit.bind(this);

    }

    onChange(data, isValid) {
        // this is a bit horrible because this.state.data is an array of objects, where
        // each object has the parameter `data`. i.e. data[0].data, data[0].isValid
        const newData = Object.assign({}, this.state.data);

        // newData[this.state.pageIndex] = {data, isValid};
        const old = newData[this.state.pageIndex].data;
        newData[this.state.pageIndex] = {
            data: _merge(old, data),
            isValid,
        };

        this.setState({data: newData});
    }

    next() {
        this.setState({pageIndex: this.state.pageIndex + 1});
    }

    prev() {
        this.setState({pageIndex: this.state.pageIndex - 1});
    }

    submit() {
        this._form.submit();
    }

    render() {
        const {pageIndex, pages} = this.state;
        const page = this.state.pages[pageIndex];
        const pageData = this.state.data[pageIndex];

        let inputs = [];

        _each(this.state.data, (pageData) => {
            _each(pageData.data, (value, name) => {
                if (value) {
                    inputs.push(<input key={name} type="hidden" name={decamelize(name)} value={value}/>);
                }
            });
        });

        _each(this.props.data, (value, name) => {
            inputs.push(<input key={name} type="hidden" name={name} value={value}/>);
        });

        // construct next, previous and submit buttons (if applicable)
        let next, previous, submit;

        if (pageIndex !== pages.length - 1) {
            next = <button disabled={!pageData.isValid} onClick={this.next}>Next</button>;
        }

        if (pageIndex !== 0) {
            previous = <button onClick={this.prev}>Previous</button>;
        }

        if (pageIndex === pages.length - 1) {
            submit = <button disabled={!pageData.isValid} onClick={this.submit}>Submit</button>;
        }

        return (
            <div>
                {React.createElement(page.component, {
                    onChange: this.onChange.bind(this),
                    data: pageData.data || undefined,
                    isValid: pageData.isValid
                })}

                {previous}
                {next}
                {submit}

                <form method="post" style={{display: 'none'}} ref={form => this._form = form}>
                    <input type="hidden" name="csrfmiddlewaretoken" value={this.props.csrfToken}/>
                    {inputs}
                </form>
            </div>
        )
    }
}
