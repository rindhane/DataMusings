import matplotlib.pyplot as plt

def get_conversion(l):
      for i in l:
        yield i*100/1000

def set_axes_details(axes,**inputs):
    x_label=inputs.get('x_label',None)
    y_label=inputs.get('y_label',None)
    color=inputs.get('color', 'tab:blue')
    fontsize=inputs.get('fontsize',5)
    labelsize=inputs.get('labelsize',5)
    axes.set_xlabel(x_label,fontsize=fontsize)
    axes.set_ylabel(y_label,fontsize=fontsize)
    axes.tick_params(axis="x", labelsize=labelsize ,color = color)
    axes.tick_params(axis='y', labelsize=labelsize, color= color)
    axes.legend(prop={'size':inputs.get('legedsize',5)})
    ax.set_title(inputs.get('title',None),fontsize= fontsize+20)
    if inputs.get('grid', None):
        ax.grid()

def plot_graph(X, label1,
               A, label2,
            x_label=None,y_label=None,
            x_top_label=None,
            title=None,
            kind1='linear',
            kind2='linear',
            file_=None):
    '''Helper functio to plot the dual plot of barh & line'''
    #setting upthe figures and axes
    fig, ax = plt.subplots(figsize=(25, 30))
    ax2 = ax.twiny()
    plot=getattr(ax,kind1, getattr(ax,'plot'))
    plot2=getattr(ax2,kind2, getattr(ax2,'plot'))
    #plotting the data on the figure
    plot(X[0],X[1],label=label1,color='green')
    plot2(A[0],A[1],label=label2, color='red')
    #configuring the x_axes properties
    ax.set_xlabel(x_label,fontsize = 30) #xlabel
    ax.tick_params(axis="x", labelsize=20)
    ax2.tick_params(axis='x',labelsize=20)
    #ax2.set_xticklabels(get_conversion(ax.get_xticks()))
    #ax2.set_xticks(ax.get_xticks())
      #axes.Axes.set_xlim()
    ax2.set_xlabel( x_top_label, fontsize = 30)
    #configuring the y_axes properties
    ax.set_ylabel(y_label, fontsize = 30, color='b')
    ax.tick_params(axis="y", labelsize=30)
      #axes.Axes.set_ylim()
    #configure axes & figure properties
      #ax.set(xlim=[-10000, 140000], xlabel=x_label, ylabel=y_label,title=title)
    ax.legend(prop={'size':30})
    ax2.legend(prop={'size':30})
    ax.grid()
    #plt.style.use('seaborn-pastel')
    plt.style.use('dark_background')
    ax.set_title(title,fontsize= 50)
    #saving the
    if file_:
      fig.savefig(file_)
    plt.show()

def figure_details(width,height):
    return {'figsize': (width,height)}

def plot_distributions(series,
                        **inputs):
    #setting upthe figures and axes
    fig, ax = plt.subplots(**figure_details(
        inputs.get('figWidth',10),inputs.get('figHeight',10)))
    ax.set_xlim([40,600])
    set_axes_details(ax,**inputs)
    plot=getattr(ax,
                inputs.get('kind','plot'),)
    plot(series, bins=inputs.get('nbins',20))
    plt.show()