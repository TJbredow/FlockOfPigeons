import os

import yaml
import jinja2
from kubernetes import client, config


kubeconfig = os.getenv("KUBECONFIG","./config")



class PigeonCluster:
    kubeconfig = os.getenv("KUBECONFIG","./config")
    namespace_prefix = "bird-"
    contexts, activecontext = config.list_kube_config_contexts(kubeconfig)

    def add_namespace(self, context: str,  namespace: client.V1Namespace):
        nsname = namespace.metadata.name
        if not nsname.startswith(self.namespace_prefix):
            return
        self.nsts[context].append(namespace.metadata.name)
    
    def check_uniform(self):
        nests = [x for x in self.nsts.values()]
        for cxt in self.nsts.values():
            if nests[0] != cxt:
                return []
        return nests[0]

    def __init__(self):
        self.nestnames = []
        cxts = [x['name'] for x in self.contexts]
        self.nsts = {x : [] for x in cxts}
        for cxt in cxts:
            config.load_kube_config(kubeconfig, cxt)
            v1 = client.CoreV1Api()
            nms = v1.list_namespace()
            for n in nms.items:
                self.add_namespace(cxt, n)
        self.nestnames = self.check_uniform()
        if not self.nestnames:
            print("Clusters are not equal, or no nests present! Proceed with caution")
        self.nests = [Nest(x) for x in self.nestnames]

class Nest:
    def validate_uniform(self):
        deps = [x.items for x in self.deps]


    def __init__(self, name):
        self.deps = dict()
        cxts = [x['name'] for x in PigeonCluster.contexts]
        for cxt in cxts:
            config.load_kube_config(PigeonCluster.kubeconfig, cxt)
            v1 = client.AppsV1Api()
            self.deps[cxt] = v1.list_namespaced_deployment(name)

        
        

if __name__ == "__main__":
    pg = PigeonCluster()
    print(pg.nsts)
    print(pg.nests[0].deps)