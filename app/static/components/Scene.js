import React from 'react';

export default class Scene extends React.Component {
    state = {
        page: 0,
    };

    render() {
        const pageIndex = this.state.page - 1;
        const content = this.props.pages[pageIndex];

        return (
            <div>
                {React.createElement(content, { onChange: this.onChange })}
                {pageIndex === 0 && <button>Next</button>}
                {pageIndex > 0 && pageIndex < pages.length - 1 && <button>Previous</button>}
                {pageIndex === pages.length - 1 && <button>Submit</button>}
            </div>
        )
    }
}