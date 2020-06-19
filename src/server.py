from flask import Flask, request, render_template, session, redirect
import pandas as pd
from types import ModuleType

app = Flask("create-features-demo", static_folder="static", template_folder="templates")

# example data 
example_df = pd.DataFrame({
    'age': [4, 23, 45, 16, 32],
    'posX': [0, 1, 2, 3, 4],
    'posY': [5, 6, 7, 8, 9],
    'class': ['class1', 'class2', 'class3','class1', 'class3']
})

defalut_columns = ['posX', 'posY', 'class']
defalut_codeBlock = '''
import numpy as np
import pandas as pd

def create_features(df):
    """The user code to create features. This function must be implemented.
    
    This is an example.

    Parameters
    ----------
    df: pandas.DataFrame
        The selected features.
    
    Returns
    ----------
    df: pandas.DataFrame
        The new features you want to create , which don't have the features already contained.
    """

    return pd.DataFrame({
        'distance': np.sqrt(df['posX'] ** 2  + df['posY'] ** 2),
    }).join(pd.get_dummies(df['class'], columns=['class'],prefix=None, prefix_sep='_'))
'''

def create_features(df, columns, codeBlock):
    in_df = df[columns]
    
    # compile the code with a module
    cf_module = ModuleType("create_features")
    compiledCodeBlock = compile(codeBlock, '<string>', 'exec')
    exec(compiledCodeBlock,cf_module.__dict__)
    
    # call the create_features function
    out_df = cf_module.create_features(in_df)
    
    return df.join(out_df)


def render(df, columns, codeBlock):
    return render_template('index.html',
        tables=[df.to_html(classes='data')],
        titles=df.columns.values,
        columns = ",".join(columns or defalut_columns),
        codeBlock = codeBlock or defalut_codeBlock
    )

@app.route('/create-features-demo',methods=["POST"])
def root():
    info = request.form.to_dict()
    columns = info.get("columns").split(",")
    codeBlock = info.get("codeBlock")
    new_df = create_features(example_df, columns, codeBlock)
    return render(new_df, columns, codeBlock)

@app.route('/')
def index():
    return render(example_df, defalut_columns, defalut_codeBlock)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)

