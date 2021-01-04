import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('dark_background')
def set_axes_details(axes,**inputs):
    x_label=inputs.get('x_label',None)
    y_label=inputs.get('y_label',None)
    color=inputs.get('color', 'tab:blue')
    fontsize=inputs.get('fontsize',5)
    labelsize=inputs.get('labelsize',5)
    rotation=inputs.get('xlabelrotation',None)
    axes.set_xlabel(x_label,fontsize=fontsize)
    axes.set_ylabel(y_label,fontsize=fontsize)
    axes.tick_params(axis="x", labelsize=labelsize ,color = color, rotation=rotation)
    axes.tick_params(axis='y', labelsize=labelsize, color= color)
    axes.legend(prop={'size': inputs.get('legendsize',5)})
    axes.set_title(inputs.get('title',None),fontsize= fontsize+20)
    axes.set_xlim(inputs.get('xlim',None))
    if inputs.get('grid', None):
        axes.grid()

def figure_details(width,height):
    return {'figsize': (width,height)}

   
def plot_inputs(inputs):
    plot_inputs={
        'hist': {
            'bins' : inputs.get('bins',None),
                }        
    }
    return plot_inputs.get(inputs.get('kind',None),{})

def is_multiple_series(kind):
    single=['hist']
    double=['plot']
    if kind in single:
        return False
    else :
        return True

def plot_graph(Xseries, Yseries=None,
                        **inputs):
    '''write utililty of graph'''
    fig, ax = plt.subplots(**figure_details(
        inputs.get('figWidth',10),inputs.get('figHeight',10)))
    plot=getattr(ax,
                inputs.get('kind','plot'),)
    if is_multiple_series(inputs.get('kind','plot')):
        plot(Xseries,Yseries,**plot_inputs(inputs),
            label=inputs.get('legendlabel',"plot1"))
    else:
        plot(Xseries,**plot_inputs(inputs),
            label=inputs.get('legendlabel',"plot1"))
    set_axes_details(ax,**inputs)
    if inputs.get('file_', None):
        fig.savefig(inputs.get('file_'))
    if inputs.get('show',False):
        plt.show()
    return fig

def plot_graph_doubleX(series1,series2,
                        **inputs):
    '''Helper functio to plot the dual plot of barh & line'''
    fig, ax = plt.subplots(**figure_details(
        inputs.get('figWidth',10),inputs.get('figHeight',10)))
    ax2 = ax.twiny()
    plot=getattr(ax,
                inputs.get('kind','plot'),)
    plot2=getattr(ax2,
                inputs.get('kind2','plot'))
    plot(series1[0],series1[1],
                label=inputs.get('legendlabel',"plot1"),
                color=inputs.get('color',"tab:green"))
    plot2(series2[0],series2[1],
                label=inputs.get('legendlabel2',"plot2"),
                color=inputs.get('color2',"tab:red"))
    set_axes_details(ax,**inputs)
    ax2.tick_params(axis='x', 
    labelsize=inputs.get('labelsize',5),
    labelcolor=inputs.get('color2',"tab:red"))
    ax2.set_xlabel( inputs.get('x_label2',None), fontsize=inputs.get('fontsize',5))
    ax2.legend(loc=2,prop={'size':inputs.get('legendsize',5)})
    if inputs.get('file_', None):
        fig.savefig(inputs.get('file_'))
    if inputs.get('show',False):
        plt.show()
    return fig

    
def plot_graph_doubleY(series1,series2,
                        **inputs):
    '''Helper functio to plot the dual plot of barh & line'''
    fig, ax = plt.subplots(**figure_details(
        inputs.get('figWidth',10),inputs.get('figHeight',10)))
    ax2 = ax.twinx()
    plot=getattr(ax,
                inputs.get('kind','plot'),)
    plot2=getattr(ax2,
                inputs.get('kind2','plot'))
    plot(series1[0],series1[1],
                label=inputs.get('legendlabel',"plot1"),
                color=inputs.get('color',"tab:green"))
    plot2(series2[0],series2[1],
                label=inputs.get('legendlabel2',"plot2"),
                color=inputs.get('color2',"tab:red"))
    set_axes_details(ax,**inputs)
    ax2.tick_params(axis='y', 
                    labelsize=inputs.get('labelsize',5),
                    labelcolor=inputs.get('color2',"tab:red"))
    ax2.set_ylabel( inputs.get('y_label2',None), fontsize=inputs.get('fontsize',5))
    ax2.tick_params(axis='x',rotation=90)
    ax2.legend(loc=0,prop={'size':inputs.get('legendsize',5)})
    if inputs.get('file_', None):
        fig.savefig(inputs.get('file_'))
    if inputs.get('show',False):
        plt.show()
    return fig

from functions import plot_scaler_abs
def plot_coeff(df,**inputs):
    scaler=plot_scaler_abs
    df=df.apply(lambda x : scaler(x) if x.name in inputs.get('scale') else x )
    height=inputs.get('height',2*2.54)
    plot=sns.catplot(x=inputs.get('x'), y=inputs.get('y'), 
                    kind= 'bar', data=df, 
                    orient='h', height=height)
    if inputs.get('file_', None):
        plot.fig.savefig(inputs.get('file_'))
    if inputs.get('show',False):
        plt.show()
    return plot

def plot_variable_corelation(df, **inputs):
    fig, ax = plt.subplots(**figure_details(
        inputs.get('figWidth',10),inputs.get('figHeight',10)))
    plot=sns.heatmap(df.corr(),ax=ax)
    if inputs.get('file_', None):
        plot.get_figure().savefig(inputs.get('file_'))
    if inputs.get('show',False):
        plt.show()
    return plot