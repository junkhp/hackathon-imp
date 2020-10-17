import numpy as np
import torch
from PIL import Image
from torchvision import transforms

from . import networks


class Pix2PixModel():
    def __init__(self, image_path):
        """
        image_path: absolute path to masked image. filename ends in "_masked.[jpg|png]".
        """
        opt = {
            'input_nc': 3,
            'output_nc': 3,
            'ngf': 64,
            'netG': 'unet_256',
            'norm': 'batch',
            'no_dropout': False,
            'init_type': 'normal',
            'init_gain': 0.02,
            'gpu_ids': []
        }
        self.use_gpu = False

        self.save_path = image_path.replace('_masked', '_inpainted')
        image = Image.open(image_path).convert('RGB')
        image = image.resize((256, 256), Image.BICUBIC)

        self.netG = networks.define_G(
            opt['input_nc'], opt['output_nc'], opt['ngf'], opt['netG'],
            opt['norm'], not opt['no_dropout'], opt['init_type'],
            opt['init_gain'], opt['gpu_ids']
        )

        self._load_networks()
        self._eval()
        self._forward(image)
        self._save_image()

    def _load_networks(self):
        weight_path = './rm_mask/inpainting/weights/weights.pth'
        state_dict = torch.load(weight_path)
        self.netG.load_state_dict(state_dict)

    def _eval(self):
        if self.use_gpu:
            self.netG.eval().cuda()
        else:
            self.netG.eval()

    def _forward(self, image):
        """
        image: np.array with shape [256, 256, 3], range [0, 255]
        """
        image = transforms.ToTensor()(image)
        image = transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))(image)
        image = image.unsqueeze(0)
        image.permute(0, 3, 1, 2)
        if self.use_gpu:
            image = image.cuda()

        with torch.no_grad():
            self.res = self.netG(image)

    def _save_image(self):
        image_tensor = self.res.data
        image_numpy = image_tensor[0].cpu().float().numpy()
        image_rgb = np.transpose(image_numpy, (1, 2, 0))
        image_rgb = ((image_rgb + 1) / 2.0) * 255.0
        image_rgb = image_rgb.astype(np.uint8)

        Image.fromarray(image_rgb).save(self.save_path)

    def get_path_to_inpainted_image(self):
        return self.save_path
