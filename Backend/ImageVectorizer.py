import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import os
import pandas as pd
import numpy as np
import io

class ImageVectorizer:
    def __init__(self, device='cpu'):
        """
        Initialize the ImageVectorizer with a trained model.

        Parameters:
            checkpoint_path (str): Path to the saved model checkpoint.
            num_classes (int): Number of output classes.
            device (str): Device to load the model on ('cpu').
        """
        self.device = device
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],  # ImageNet mean
                                 std=[0.229, 0.224, 0.225])  # ImageNet std
        ])
        checkpoint_path = os.path.join(os.path.dirname(__file__), 'best_model.pth')
        num_classes = 161
        self.model = self._load_model(checkpoint_path, num_classes)
        
    def _load_model(self, checkpoint_path, num_classes):
        """
        Load the trained CustomResNet model from the checkpoint.
        """
        model = torch.load(checkpoint_path, map_location=self.device)
        model.to(self.device)
        model.eval()
        return model

    def vectorize_image(self, image_input):
        """
        Processes the input image and returns a 256-dimensional feature vector.

        Parameters:
            image_input (str or PIL.Image.Image): Path to the image file or a PIL Image object.

        Returns:
            numpy.ndarray: 256-dimensional feature vector.
        """
        # Load the image
        if isinstance(image_input, str):
            if not os.path.exists(image_input):
                raise FileNotFoundError(f"Image file not found at '{image_input}'")
            image = Image.open(image_input).convert("RGB")
        elif isinstance(image_input, Image.Image):
            image = image_input.convert("RGB")
        else:
            raise ValueError("image_input must be a file path or a PIL.Image.Image object.")

        # Apply transformations
        image = self.transform(image).unsqueeze(0).to(self.device)  # Add batch dimension

        # Extract the feature vector
        with torch.no_grad():
            vector = self.model.get_vector(image)
            vector = vector.cpu().numpy().flatten()

        return vector


class CustomResNet(nn.Module):
    def __init__(self, num_classes):
        super(CustomResNet, self).__init__()
        base_model = models.resnet34(pretrained=True)
        self.base = nn.Sequential(*list(base_model.children())[:-1])  # Remove the final classification layer
        self.fc_layers = nn.Sequential(
            nn.Linear(512, 512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, 512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, 512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, 512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, 512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, 512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, 512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, 512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, 512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, 512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, 512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, 512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, 256),  # Vector layer
            nn.ReLU(), nn.Dropout(0.5),
        )
        self.output_layer = nn.Linear(256, num_classes)

    def forward(self, x):
        x = self.base(x).flatten(1)  # Extract features
        x = self.fc_layers(x)        # Vectorization layers
        return self.output_layer(x)  # Classification layer

    def get_vector(self, x):
        x = self.base(x).flatten(1)
        for layer in self.fc_layers:
            x = layer(x)
            if isinstance(layer, nn.Linear) and layer.out_features == 256:
                break  # Stop after the Linear(512, 256) layer
        return x


# Usage Example
if __name__ == "__main__":
    # Initialize ImageVectorizer
    vectorizer = ImageVectorizer(device='cpu')
    
    # Example of vectorizing a single image
    image_path = r"C:\Users\HomePC\Desktop\poster_image.jpg"  # Replace with your image path
    vector = vectorizer.vectorize_image(image_path)
    print(f"Vector shape: {vector.shape}")
    print(f"Vector: {vector}")
