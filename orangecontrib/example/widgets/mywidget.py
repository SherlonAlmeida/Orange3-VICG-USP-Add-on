# -*- coding: utf-8 -*-
from Orange.data import ContinuousVariable, DiscreteVariable, StringVariable
from Orange.data import Domain, Table
import numpy as np
import mppy
import sys
import Orange.data
from Orange.widgets import widget, gui
from Orange.widgets.utils.signals import Input, Output

class OWDataSamplerA(widget.OWWidget):
    name = "LSP"
    description = "Multidimensional projection technique to group similar data in low dimension, preserving their similarities."
    description += "\n\n Paulovich, Fernando V., et al. \"Least square projection: A fast high-precision multidimensional projection technique and its application to document mapping.\" IEEE Transactions on Visualization and Computer Graphics 14.3 (2008): 564-575."
    icon = "icons/lsp_icon.png"
    priority = 10

    class Inputs:
        data = Input("Data", Orange.data.Table)

    class Outputs:
        #sample = Output("Sampled Data", Orange.data.Table)
        out = Output("Data", Orange.data.Table)

    want_main_area = False
    commitOnChange = 0

    def __init__(self):
        super().__init__()
        
        self.dataset = None
        self.neighborhood = 15
        
        # Graphical User Interface - GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something.")
        
        gui.separator(self.controlArea)
        self.optionsBox = gui.widgetBox(self.controlArea, "Options")
        gui.spin(
            self.optionsBox,
            self,
            "neighborhood",
            minv=5,
            maxv=100,
            step=5,
            label="Neighborhood:",
            callback=[self.selection, self.checkCommit],
        )
        gui.checkBox(self.optionsBox, self, "commitOnChange", "Commit data on selection change")
        gui.button(self.optionsBox, self, "Commit", callback=self.commit)
        self.optionsBox.setDisabled(True)
    
    @Inputs.data
    def set_data(self, dataset):
        if dataset is not None:
            self.dataset = dataset
            self.infoa.setText("%d instances in input data set" % len(dataset))
            self.optionsBox.setDisabled(False)
            self.selection()
        else:
            self.dataset = None
            self.optionsBox.setDisabled(False)
            self.infoa.setText("No data on input yet, waiting to get something.")
        self.commit()
    
    def selection(self):
        if self.dataset is None:
            return
    
    def commit(self):
        out_data = self.get_lsp_results(self.dataset)
        #self.Outputs.sample.send(out_data)
        self.Outputs.out.send(out_data)
        

    def checkCommit(self):
        if self.commitOnChange:
            self.commit()

    def get_lsp_results(self, in_data):
        attr = in_data.domain.attributes    #Obtem os Atributos provenientes do Workflow
        target = in_data.domain.class_vars  #Obtem as Classes provenientes do Workflow
        meta = in_data.domain.metas			#Obtem os Meta dados provenientes do Workflow
        data = np.array(in_data)			#Converte os dados para Numpy Array (Pois a LSP da MPPY trabalha com dados Numpy)
        coordinates_2d = mppy.lsp_2d(data, n_neighbors=self.neighborhood)	#Calcula as coordenadas em dimensao 2D com o LSP
        
        """ Obtem os Atributos provenientes do Workflow e adiciona os demais"""
        X = []
        for j in range(len(in_data)):
            aux = []
            for i in range(len(in_data.domain.attributes)):
                attr_name = in_data.domain.attributes[i].name
                attr_index = in_data.domain.index(attr_name)
                attr_data  = in_data[j, attr_index]
                aux.append(attr_data)
            X.append(aux)
        
        """ Obtem as Classes provenientes do Workflow e adiciona os demais"""
        Y = []
        for j in range(len(in_data)):
            aux = []
            for i in range(len(in_data.domain.class_vars)):
                values_name = in_data.domain.class_vars[i].name
                values_index = in_data.domain.index(values_name)
                values_data  = in_data[j, values_index]
                aux.append(values_data)
            Y.append(aux)
        
        """ Obtem os Meta dados provenientes do Workflow e adiciona os demais"""
        M = []
        for j in range(len(in_data)):
            aux = []
            for i in range(len(in_data.domain.metas)):
                meta_name = in_data.domain.metas[i].name
                meta_index = in_data.domain.index(meta_name)
                meta_data  = in_data[j, meta_index]
                aux.append(meta_data)
            aux.append(coordinates_2d[j][0]) #Coordenada LSP-x
            aux.append(coordinates_2d[j][1]) #Coordenada LSP-y
            M.append(aux)
        
        """Adiciona as informacoes do LSP nos Meta dados, para passar a frente no workflow"""
        meta = meta + (ContinuousVariable("LSP-x"),)
        meta = meta + (ContinuousVariable("LSP-y"),)
        
        """ Domain(...)
        	Attributes: attributes (list of Variable) – a list of attributes
        	Classes: class_vars (Variable or list of Variable) – target variable or a list of target variables
        	Metas: metas (list of Variable) – a list of meta attributes
        	Source: source (Orange.data.Domain) – the source domain for attributes """
        domain = Domain(
        		attr,
        		target,
        		meta,
        		None
            )
        
        """ Table.from_numpy(...)
        	Domain: domain (Orange.data.Domain) – the domain for the new table
        	Values: X (np.array) – array with attribute values
        	Classes: Y (np.array) – array with class values
        	#Metas: metas (np.array) – array with meta attributes
        	Weights: W (np.array) – array with weights """
        out_data = Table.from_numpy(
                        domain,
                        X,
                        Y,
                        M,
                        None
                    )
        
        return out_data

"""Debugging the widget"""
"""
def main(argv=sys.argv):
    from AnyQt.QtWidgets import QApplication
    app = QApplication(list(argv))
    args = app.arguments()
    if len(args) > 1:
        filename = args[1]
    else:
        filename = "iris"

    ow = OWDataSamplerA()
    ow.show()
    ow.raise_()

    dataset = Orange.data.Table(filename)
    ow.set_data(dataset)
    ow.handleNewSignals()
    app.exec_()
    ow.set_data(None)
    ow.handleNewSignals()
    return 0


if __name__ == "__main__":
    sys.exit(main())
"""