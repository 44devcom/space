from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime


class CarBase(BaseModel):
    context: Optional[str] = Field(None, max_length=500, description="JSON-LD context")
    type: Optional[str] = Field("Car", max_length=100, description="JSON-LD type")
    sitemapId: Optional[int] = Field(None, description="Reference to sitemap")
    url: Optional[str] = Field(None, max_length=1000, description="Listing URL")
    category: Optional[str] = Field(None, max_length=100, description="Vehicle category")
    brand: Optional[str] = Field(None, max_length=100, description="Vehicle brand")
    model: Optional[str] = Field(None, max_length=100, description="Vehicle model")
    details: Optional[str] = Field(None, description="Additional details")
    description: Optional[str] = Field(None, description="Vehicle description")
    title: Optional[str] = Field(None, max_length=500, description="Listing title")
    adSellerName: Optional[str] = Field(None, max_length=200, description="Seller name")
    email: Optional[EmailStr] = Field(None, max_length=255, description="Contact email")
    phonePrimary: Optional[str] = Field(None, max_length=20, description="Primary phone number")
    phoneSecondary: Optional[str] = Field(None, max_length=20, description="Secondary phone number")
    typeClasses: Optional[str] = Field(None, max_length=200, description="Type classes")
    notes: Optional[Dict[str, Any]] = Field(None, description="Additional notes stored as JSON")


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    context: Optional[str] = Field(None, max_length=500)
    type: Optional[str] = Field(None, max_length=100)
    sitemapId: Optional[int] = None
    url: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    details: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = Field(None, max_length=500)
    adSellerName: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = Field(None, max_length=255)
    phonePrimary: Optional[str] = Field(None, max_length=20)
    phoneSecondary: Optional[str] = Field(None, max_length=20)
    typeClasses: Optional[str] = Field(None, max_length=200)
    notes: Optional[Dict[str, Any]] = None


class CarResponse(CarBase):
    id: int = Field(..., description="Primary key identifier")
    createdAt: Optional[datetime] = Field(None, description="Record creation timestamp")
    updatedAt: Optional[datetime] = Field(None, description="Record update timestamp")
    deletedAt: Optional[datetime] = Field(None, description="Soft delete timestamp")

    class Config:
        from_attributes = True


