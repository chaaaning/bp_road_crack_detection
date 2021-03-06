import torch
import torch.nn.functional as F
from tqdm import tqdm

from utils.dice_score import multiclass_dice_coeff, dice_coeff

<<<<<<< HEAD
<<<<<<<< HEAD:1_모델링/PAN/evaluate.py
def evaluate(net, dataloader, device):
========

def evaluate(net, res, mc, dataloader, device):
    res.eval()
>>>>>>>> b21dbb31461ff9a9454c5184dcdb918fd063a3c7:pan modeling/evaluate.py
=======

def evaluate(net, res, mc, dataloader, device):
    res.eval()
>>>>>>> b21dbb31461ff9a9454c5184dcdb918fd063a3c7
    net.eval()
    num_val_batches = len(dataloader)
    n_classes = 2
    dice_score = 0

    # iterate over the validation set
    for batch in tqdm(dataloader, total=num_val_batches, desc='Validation round', unit='batch', leave=False):
        image, mask_true = batch['image'], batch['mask']
        # move images and labels to correct device and type
<<<<<<< HEAD

        with torch.no_grad():
            image = image.to(device=device, dtype=torch.float32)
            mask_true = mask_true.to(device=device, dtype=torch.float32)

=======
        image = image.to(device=device, dtype=torch.float32)
        mask_true = mask_true.to(device=device, dtype=torch.long)
        mask_true = F.one_hot(mask_true, n_classes).permute(0, 3, 1, 2).float()

        with torch.no_grad():
>>>>>>> b21dbb31461ff9a9454c5184dcdb918fd063a3c7
            # predict the mask
            fms_blob, z = res(image)
            out_ss = net(fms_blob[::-1])
            mask_pred = mc(out_ss)

<<<<<<< HEAD
            # true mask를 먼저 interpolate 시키고, 그 다음 one-hot encoding을 진행.
            # mask_true = F.interpolate(mask_true, scale_factor=0.25, mode='nearest')
            mask_true = F.one_hot(mask_true.long().squeeze(1), n_classes).permute(0, 3, 1, 2).float()

=======
>>>>>>> b21dbb31461ff9a9454c5184dcdb918fd063a3c7
            # convert to one-hot format
            if n_classes == 1:
                mask_pred = (F.sigmoid(mask_pred) > 0.5).float()
                # compute the Dice score
                dice_score += dice_coeff(mask_pred, mask_true, reduce_batch_first=False)
            else:
                mask_pred = F.one_hot(mask_pred.argmax(dim=1), n_classes).permute(0, 3, 1, 2).float()
                # compute the Dice score, ignoring background
                dice_score += multiclass_dice_coeff(mask_pred[:, 1:, ...], mask_true[:, 1:, ...], reduce_batch_first=False)

<<<<<<< HEAD
=======
           

>>>>>>> b21dbb31461ff9a9454c5184dcdb918fd063a3c7
    net.train()

    # Fixes a potential division by zero error
    if num_val_batches == 0:
        return dice_score
    return dice_score / num_val_batches
