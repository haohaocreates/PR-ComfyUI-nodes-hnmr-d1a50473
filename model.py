import folder_paths
from comfy.sd import load_torch_file

class StateDictLoader:
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'ckpt_name': (folder_paths.get_filename_list("checkpoints"), )
            }
        }
    
    RETURN_TYPES = ('DICT',)
    
    FUNCTION = 'execute'

    CATEGORY = 'loaders'

    def execute(self, ckpt_name: str):
        ckpt_path = folder_paths.get_full_path('checkpoints', ckpt_name)
        sd = load_torch_file(ckpt_path)
        return (sd,)
    

class Dict2Model:
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'weights': ('DICT', ),
                'config_name': (folder_paths.get_filename_list('configs'), ),
            }
        }
    
    RETURN_TYPES = ('MODEL', 'CLIP', 'VAE')
    
    FUNCTION = 'execute'

    CATEGORY = 'model'

    def execute(self, weights: dict, config_name: str):
        config_path = folder_paths.get_full_path("configs", config_name)
        
        def load_torch_file_hook(*args, **kwargs):
            return weights
        
        import comfy.sd as sd
        load_torch_file_org = sd.load_torch_file
        setattr(sd, 'load_torch_file', load_torch_file_hook)
        
        try:
            return sd.load_checkpoint(config_path, None, output_vae=True, output_clip=True, embedding_directory=folder_paths.get_folder_paths("embeddings"))
        finally:
            setattr(sd, 'load_torch_file', load_torch_file_org)

